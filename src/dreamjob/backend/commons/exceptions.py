class RecommendationException(Exception):
    pass


class NotEnoughVacanciesToRec(RecommendationException):
    """if not enough good quality vacs when recommending (model decides good quality)"""
    pass


class VacanciesAreOutOfDate(RecommendationException):
    """if the freshest vacancy in db was created/updated 14 days ago"""
    pass
