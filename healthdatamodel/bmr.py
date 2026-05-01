"""
BMR (Basal Metabolic Rate) computation and lookup.

This module contains both the low-level Mifflin-St Jeor calculation
and the higher-level ``get_bmr()`` helper that resolves BMR from
age and gender.  It has no internal dependencies beyond the standard
library.
"""

from __future__ import annotations

import logging
from datetime import date, datetime, timezone

logger = logging.getLogger(__name__)

DEFAULT_BMR: float = 2000.0

# median height and weight in cm and kg
# ref: https://www.cdc.gov/nchs/fastats/body-measurements.htm
HEIGHT_WEIGHT = {
    "M": {
        "18": (71, 175.5),
        "19": (77, 176.1),
        "20-29": (81.3, 176.0),
        "30-39": (89.7, 176.7),
        "40-49": (90.5, 176.5),
        "50-59": (89.6, 175.3),
        "60-69": (89.5, 174.3),
        "70-79": (85.3, 173.1),
        "80+": (79.6, 170.3),
    },
    "F": {
        "18": (62.7, 162.3),
        "19": (65.7, 161.2),
        "20-29": (69.5, 162.8),
        "30-39": (73.3, 162.6),
        "40-49": (75.2, 162.6),
        "50-59": (74.6, 160.9),
        "60-69": (75.1, 160.8),
        "70-79": (73.2, 157.9),
        "80+": (66.3, 155.8),
    },
}


def calculate_bmr(age: int, gender: str, weight: float, height: float) -> float:
    """
    Calculate BMR using the Mifflin-St Jeor equation.

    Args:
        age: The user's age in years.
        gender: ``"M"`` for male or ``"F"`` for female.
        weight: The user's weight in kilograms.
        height: The user's height in centimeters.

    Returns:
        Daily BMR in kcal.
    """
    if gender.upper() == "M":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    return bmr


def lookup_bmr(age: int, gender: str) -> float:
    """
    Look up BMR from median height/weight tables for *age* and *gender*.
    """
    if age < 20:
        age_str = str(age)
    elif age < 30:
        age_str = "20-29"
    elif age < 40:
        age_str = "30-39"
    elif age < 50:
        age_str = "40-49"
    elif age < 60:
        age_str = "50-59"
    elif age < 70:
        age_str = "60-69"
    elif age < 80:
        age_str = "70-79"
    else:
        age_str = "80+"

    # calls to here have already ruled out gender other than M or F
    bmr = calculate_bmr(age, gender, *HEIGHT_WEIGHT[gender][age_str])

    logger.info(f"for {age_str=}, {gender=}, we have {bmr=}")

    return bmr


def age_from_dob(dob: date) -> int:
    """Compute integer age from a date-of-birth."""
    today = datetime.now(timezone.utc).date()
    birthday_this_year = (today.month, today.day) < (dob.month, dob.day)
    return today.year - dob.year - birthday_this_year


def get_bmr(
    age: int | None = None,
    gender: str = "",
    *,
    default: float = DEFAULT_BMR,
) -> float:
    """Return daily BMR for the given *age* and *gender*, or *default*.

    Callers are responsible for resolving age from whatever source they
    have (e.g. a date-of-birth field).  Use :func:`age_from_dob` if you
    need to convert a DOB to an integer age before calling this function.

    Parameters
    ----------
    age:
        User's age in years.  ``None`` means unknown.
    gender:
        Expected ``"M"`` or ``"F"``; anything else returns *default*.
    default:
        Fallback BMR when age/gender are insufficient.
    """
    if age is None or gender == "":
        logger.warning("No age or gender supplied, returning default BMR")
        return default
    if gender.upper() not in ("M", "F"):
        logger.warning("Gender not M or F (%s), returning default BMR", gender)
        return default
    if age < 18:
        logger.warning("Age under 18, returning default BMR")
        return default
    logger.info("Using BMR from lookup table")
    return lookup_bmr(age, gender)
