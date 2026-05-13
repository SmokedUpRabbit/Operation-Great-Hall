from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Literal
from datetime import date

AggregationLevel = Literal[
    "worker", "role", "line", "team", "shift", "day", "week", "facility"
]
ProductionMode = Literal[
    "barrel", "rack", "part_count", "mass_throughput", "hybrid"
]
PricingMode = Literal["mass", "unit", "auto"]


@dataclass
class BusinessTierConfig:
    name: str = "business"
    currency: str = "USD"
    default_shift_minutes: int = 480
    default_payroll_tax_fraction: float = 0.0765
    default_benefits_per_shift: float = 0.0
    default_opex_fraction: float = 0.35
    default_tax_overhead_fraction: float = 0.10
    default_scrap_fraction: float = 0.0
    default_rework_fraction: float = 0.0
    pricing_mode: PricingMode = "auto"
    allow_negative_net_share: bool = True
    strict_validation: bool = True


@dataclass
class ExtractionInputs:
    event_id: str
    line_id: str
    role_id: str
    date: str
    shift_label: str
    aggregation_level: AggregationLevel = "shift"
    production_mode: ProductionMode = "mass_throughput"
    production_units: float = 0.0
    weights_lbs: List[float] = field(default_factory=list)
    total_weight_lbs: Optional[float] = None
    downtime_minutes: float = 0.0
    shift_minutes: int = 480
    wage_per_hour: float = 0.0
    benefits_per_shift: float = 0.0
    payroll_tax_fraction: float = 0.0765
    price_per_lb: Optional[float] = None
    price_per_unit: Optional[float] = None
    opex_fraction: float = 0.35
    tax_overhead_fraction: float = 0.10
    scrap_fraction: float = 0.0
    rework_fraction: float = 0.0
    notes: str = ""

    def resolved_total_weight_lbs(self) -> float:
        if self.total_weight_lbs is not None:
            return float(self.total_weight_lbs)
        return float(sum(self.weights_lbs))


class ValidationError(ValueError):
    pass


@dataclass
class BusinessTierEngine:
    config: BusinessTierConfig = field(default_factory=BusinessTierConfig)

    def build_event(self, **kwargs: Any) -> ExtractionInputs:
        payload = dict(kwargs)
        payload.setdefault("shift_minutes", self.config.default_shift_minutes)
        payload.setdefault("benefits_per_shift", self.config.default_benefits_per_shift)
        payload.setdefault("payroll_tax_fraction", self.config.default_payroll_tax_fraction)
        payload.setdefault("opex_fraction", self.config.default_opex_fraction)
        payload.setdefault("tax_overhead_fraction", self.config.default_tax_overhead_fraction)
        payload.setdefault("scrap_fraction", self.config.default_scrap_fraction)
        payload.setdefault("rework_fraction", self.config.default_rework_fraction)
        return ExtractionInputs(**payload)

    def validate(self, event: ExtractionInputs) -> None:
        if event.shift_minutes <= 0:
            raise ValidationError("shift_minutes must be > 0")
        if event.downtime_minutes < 0:
            raise ValidationError("downtime_minutes must be >= 0")
        if event.downtime_minutes > event.shift_minutes:
            raise ValidationError("downtime_minutes cannot exceed shift_minutes")
        if event.production_units < 0:
            raise ValidationError("production_units must be >= 0")
        if event.total_weight_lbs is None and not event.weights_lbs and event.production_mode in {"barrel", "rack", "mass_throughput", "hybrid"}:
            raise ValidationError("mass-based events require total_weight_lbs or weights_lbs")
        if event.price_per_lb is None and event.price_per_unit is None:
            raise ValidationError("at least one of price_per_lb or price_per_unit is required")
        for name in [
            "payroll_tax_fraction",
            "opex_fraction",
            "tax_overhead_fraction",
            "scrap_fraction",
            "rework_fraction",
        ]:
            value = getattr(event, name)
            if self.config.strict_validation and not (0 <= value <= 1):
                raise ValidationError(f"{name} must be between 0 and 1")

    @staticmethod
    def _safe_div(numerator: float, denominator: float) -> Optional[float]:
        if denominator == 0:
            return None
        return numerator / denominator

    def compute(self, event: ExtractionInputs) -> Dict[str, Any]:
        self.validate(event)

        resolved_total_weight_lbs = event.resolved_total_weight_lbs()
        shift_hours = event.shift_minutes / 60.0
        production_minutes = event.shift_minutes - event.downtime_minutes
        if production_minutes < 0:
            raise ValidationError("production_minutes computed below zero")
        production_hours = production_minutes / 60.0

        avg_lbs_per_unit = self._safe_div(resolved_total_weight_lbs, event.production_units)
        units_per_hour_active = self._safe_div(event.production_units, production_hours)
        units_per_hour_shift = self._safe_div(event.production_units, shift_hours)

        gross_revenue_mass = None if event.price_per_lb is None else resolved_total_weight_lbs * event.price_per_lb
        gross_revenue_unit = None if event.price_per_unit is None else event.production_units * event.price_per_unit

        if self.config.pricing_mode == "mass":
            gross_revenue = gross_revenue_mass
        elif self.config.pricing_mode == "unit":
            gross_revenue = gross_revenue_unit
        else:
            gross_revenue = gross_revenue_mass if gross_revenue_mass is not None else gross_revenue_unit

        if gross_revenue is None:
            raise ValidationError("gross_revenue could not be resolved")

        revenue_per_hour_shift = self._safe_div(gross_revenue, shift_hours)
        revenue_per_hour_active = self._safe_div(gross_revenue, production_hours)

        opex_cost = gross_revenue * event.opex_fraction
        tax_overhead_cost = gross_revenue * event.tax_overhead_fraction
        scrap_cost = gross_revenue * event.scrap_fraction
        rework_cost = gross_revenue * event.rework_fraction
        base_labor_cost_shift = event.wage_per_hour * shift_hours
        benefits_cost_shift = event.benefits_per_shift
        payroll_tax_cost_shift = base_labor_cost_shift * event.payroll_tax_fraction
        total_labor_cost_shift = base_labor_cost_shift + benefits_cost_shift + payroll_tax_cost_shift

        firm_net_shift = gross_revenue - opex_cost - tax_overhead_cost - scrap_cost - rework_cost - total_labor_cost_shift
        firm_net_per_hour = self._safe_div(firm_net_shift, shift_hours)
        worker_value_received_shift = total_labor_cost_shift
        worker_value_received_per_hour = self._safe_div(total_labor_cost_shift, shift_hours)

        net_retention_ratio = self._safe_div(firm_net_per_hour, worker_value_received_per_hour) if firm_net_per_hour is not None and worker_value_received_per_hour is not None else None
        value_gap_shift = firm_net_shift - worker_value_received_shift
        value_gap_hour = None if firm_net_per_hour is None or worker_value_received_per_hour is None else firm_net_per_hour - worker_value_received_per_hour
        labor_share_of_gross = self._safe_div(worker_value_received_shift, gross_revenue)
        firm_share_of_gross_net = self._safe_div(firm_net_shift, gross_revenue)
        extraction_index = self._safe_div(value_gap_hour, worker_value_received_per_hour) if value_gap_hour is not None and worker_value_received_per_hour is not None else None

        return {
            "meta": {
                "tier": self.config.name,
                "currency": self.config.currency,
                "pricing_mode": self.config.pricing_mode,
            },
            "inputs": asdict(event),
            "derived": {
                "resolved_total_weight_lbs": resolved_total_weight_lbs,
                "shift_hours": shift_hours,
                "production_minutes": production_minutes,
                "production_hours": production_hours,
                "avg_lbs_per_unit": avg_lbs_per_unit,
                "units_per_hour_active": units_per_hour_active,
                "units_per_hour_shift": units_per_hour_shift,
            },
            "revenue": {
                "gross_revenue_mass": gross_revenue_mass,
                "gross_revenue_unit": gross_revenue_unit,
                "gross_revenue": gross_revenue,
                "revenue_per_hour_shift": revenue_per_hour_shift,
                "revenue_per_hour_active": revenue_per_hour_active,
            },
            "costs": {
                "opex_cost": opex_cost,
                "tax_overhead_cost": tax_overhead_cost,
                "scrap_cost": scrap_cost,
                "rework_cost": rework_cost,
                "base_labor_cost_shift": base_labor_cost_shift,
                "benefits_cost_shift": benefits_cost_shift,
                "payroll_tax_cost_shift": payroll_tax_cost_shift,
                "total_labor_cost_shift": total_labor_cost_shift,
            },
            "net": {
                "firm_net_shift": firm_net_shift,
                "firm_net_per_hour": firm_net_per_hour,
                "worker_value_received_shift": worker_value_received_shift,
                "worker_value_received_per_hour": worker_value_received_per_hour,
            },
            "extraction_metrics": {
                "net_retention_ratio": net_retention_ratio,
                "value_gap_shift": value_gap_shift,
                "value_gap_hour": value_gap_hour,
                "labor_share_of_gross": labor_share_of_gross,
                "firm_share_of_gross_net": firm_share_of_gross_net,
                "exchange_statement": None if net_retention_ratio is None else f"For every $1.00 returned to labor per hour, the firm retains {net_retention_ratio:.4f} dollars in net profit per hour.",
                "extraction_index": extraction_index,
            },
        }

    def compute_many(self, events: List[ExtractionInputs]) -> List[Dict[str, Any]]:
        return [self.compute(event) for event in events]

    def rollup(self, reports: List[Dict[str, Any]], group_label: str = "aggregate") -> Dict[str, Any]:
        if not reports:
            raise ValidationError("reports cannot be empty")

        gross_revenue = sum(r["revenue"]["gross_revenue"] or 0.0 for r in reports)
        total_labor = sum(r["costs"]["total_labor_cost_shift"] or 0.0 for r in reports)
        firm_net = sum(r["net"]["firm_net_shift"] or 0.0 for r in reports)
        total_shift_hours = sum(r["derived"]["shift_hours"] or 0.0 for r in reports)
        total_production_hours = sum(r["derived"]["production_hours"] or 0.0 for r in reports)
        total_units = sum(r["inputs"]["production_units"] or 0.0 for r in reports)
        total_weight = sum(r["derived"]["resolved_total_weight_lbs"] or 0.0 for r in reports)

        firm_net_per_hour = self._safe_div(firm_net, total_shift_hours)
        labor_per_hour = self._safe_div(total_labor, total_shift_hours)
        net_retention_ratio = self._safe_div(firm_net_per_hour, labor_per_hour) if firm_net_per_hour is not None and labor_per_hour is not None else None

        return {
            "group_label": group_label,
            "event_count": len(reports),
            "totals": {
                "gross_revenue": gross_revenue,
                "total_labor_cost_shift": total_labor,
                "firm_net_shift": firm_net,
                "total_shift_hours": total_shift_hours,
                "total_production_hours": total_production_hours,
                "production_units": total_units,
                "resolved_total_weight_lbs": total_weight,
            },
            "aggregate_metrics": {
                "revenue_per_hour_shift": self._safe_div(gross_revenue, total_shift_hours),
                "revenue_per_hour_active": self._safe_div(gross_revenue, total_production_hours),
                "firm_net_per_hour": firm_net_per_hour,
                "worker_value_received_per_hour": labor_per_hour,
                "labor_share_of_gross": self._safe_div(total_labor, gross_revenue),
                "firm_share_of_gross_net": self._safe_div(firm_net, gross_revenue),
                "net_retention_ratio": net_retention_ratio,
                "value_gap_shift": firm_net - total_labor,
                "value_gap_hour": None if firm_net_per_hour is None or labor_per_hour is None else firm_net_per_hour - labor_per_hour,
            },
        }


def business_tier_engine(**config_kwargs):
    return BusinessTierEngine(config=BusinessTierConfig(**config_kwargs))


if __name__ == "__main__":
    engine = business_tier_engine(name="business")
    event = engine.build_event(
        event_id="demo-001",
        line_id="cln",
        role_id="operator",
        date=str(date.today()),
        shift_label="night",
        aggregation_level="shift",
        production_mode="barrel",
        production_units=32,
        weights_lbs=[900, 900, 2100, 480, 2100, 800, 1500],
        downtime_minutes=105,
        wage_per_hour=18.0,
        benefits_per_shift=12.0,
        price_per_lb=0.42,
        opex_fraction=0.35,
        tax_overhead_fraction=0.10,
        scrap_fraction=0.02,
        rework_fraction=0.01,
        notes="Demo event",
    )
    from pprint import pprint
    pprint(engine.compute(event))
