from pydantic import BaseModel
from typing import Optional
from fractions import Fraction


class Ballot(BaseModel):
    """
    id (optional string): assigned ballot id
    ranking (list): list of candidate ranking
    weight (float/fraction): weight assigned to a given a ballot
    voters (optional list): list of voters who cast a given a ballot
    """

    id: Optional[str] = None
    ranking: list[set]
    weight: Fraction
    voters: Optional[set[str]] = None

    class Config:
        arbitrary_types_allowed = True

        
class RangeBallot(BaseModel):
    """
    id (optional string): assigned ballot id
    scores (list): list of candidate scores {candidate : scores}
    weight (float/fraction): weight assigned to a given a ballot
    voters (optional list): list of voters who cast a given a ballot
    """

    id: Optional[str] = None
    scoring: dict[str, int]
    weight: Fraction
    voters: Optional[set[str]] = None

    class Config:
        arbitrary_types_allowed = True
