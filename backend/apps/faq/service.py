from typing import List, Optional
from asgiref.sync import sync_to_async

from apps.faq.models import FAQTheme, FAQProblem


class FAQThemeService:
    @staticmethod
    @sync_to_async
    def get_themes() -> List[FAQTheme]:
        themes = FAQTheme.objects.all()
        return list(themes)
    

class FAQProblemService:

    @staticmethod
    @sync_to_async
    def get_problem(problem_id: int) -> FAQProblem:
        try:
            return FAQProblem.objects.get(id=problem_id)
        except FAQProblem.DoesNotExist:
            return None

    @staticmethod
    @sync_to_async
    def get_problems_by_theme(theme_id: int) -> List[FAQProblem]:
        problems = FAQProblem.objects.filter(theme__id=theme_id)
        return list(problems)