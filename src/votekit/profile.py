from ballot import Ballot
from ballot import RangeBallot
from typing import Optional
from pydantic import BaseModel, validator
from fractions import Fraction

# from functools import cache


class PreferenceProfile(BaseModel):
    """
    ballots (list of allots): ballots from an election
    rangeballots (list of allots): range ballots from an election
    candidates (list): list of candidates, can be user defined
    """

    ballots: list[Ballot]
    #rangeballots: Optional[list[RangeBallot]] = None 
    candidates: Optional[list] = None

    @validator("candidates")
    def cands_must_be_unique(cls, cands: list) -> list:
        if not len(set(cands)) == len(cands) and cands is not None:
            raise ValueError("all candidates must be unique")
        return cands

    def get_ballots(self) -> list[Ballot]:
        """
        Returns list of ballots
        """
        return self.ballots

    # @cache
    # fix type casting error
    def get_candidates(self) -> list[set]:
        """
        Returns list of unique candidates
        """
        if self.candidates is not None:
            return self.candidates

        unique_cands: set = set()
        for ballot in self.ballots:
            unique_cands.update(*ballot.ranking)

        return list(unique_cands)

    # can also cache
    def num_ballots(self) -> Fraction:
        """
        Assumes weights correspond to number of ballots given to a ranking
        """
        num_ballots = Fraction(0)
        for ballot in self.ballots:
            num_ballots += ballot.weight

        return num_ballots

    def to_dict(self) -> dict:
        """
        Converts ballots to dictionary with keys (ranking) and values
        the corresponding total weights
        """
        di: dict = {}
        for ballot in self.ballots:
            if str(ballot.ranking) not in di.keys():
                di[str(ballot.ranking)] = Fraction(0)
            di[str(ballot.ranking)] += ballot.weight

        return di

######################################################################################################
                                    # Altered for Range Ballot #
######################################################################################################
   

    def get_rangeballots(self) -> list[RangeBallot]:
        """
        #Returns list of range ballots
        """
        return self.rangeballots

    # @cache
    # fix type casting error
    def get_rangecandidates(self) -> list[set]:
        """
        #Returns list of unique candidates in Range Voting election
        """
        if self.candidates is not None:
            return self.candidates

        unique_cands: set = set()
        for ballot in self.rangeballots:
            unique_cands.update(*ballot.scoring)

        return list(unique_cands)

    # can also cache
    def num_rangeballots(self) -> Fraction:
        """
        #Assumes weights correspond to number of range ballots given to a scoring
        """
        num_ballots = Fraction(0)
        for ballot in self.rangeballots:
            num_ballots += ballot.weight

        return num_ballots

    def to_rangedict(self) -> dict:
        """
        #Converts range ballots to dictionary with keys (scoring) 
        #and values the corresponding total weights
        """
        di: dict = {}
        for ballot in self.rangeballots:
            if str(ballot.scoring) not in di.keys():
                di[str(ballot.ranking)] = Fraction(0)
            di[str(ballot.scoring)] += ballot.weight

        return di

        
    class Config:
        arbitrary_types_allowed = True

    # def __init__(self, ballots, candidates):
    #     """
    #     Args:
    #         ballots (list of Ballot): a list of ballots in the election
    #         candidates (list of Candidates): a list of candidates in the election
    #     """
    #     self.id = uuid.uuid4()
    #     self.ballots = ballots
    #     self.candidates = candidates
    #     self.ballot_weights = [b.score for b in ballots]
