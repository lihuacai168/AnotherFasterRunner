from fastrunner import models


def get_counter(model, pk=None):
    """
    统计相关表长度
    """
    if pk:
        return model.objects.filter(project__id=pk).count()
    else:
        return model.objects.count()


def get_project_detail(pk):
    """
    项目详细统计信息
    """
    api_count = get_counter(models.API, pk=pk)
    suite_count = get_counter(models.Suite, pk=pk)
    case_count = get_counter(models.Case, pk=pk)
    team_count = get_counter(models.Team, pk=pk)
    config_count = get_counter(models.Config, pk=pk)

    return {
        "api_count": api_count,
        "suite_count": suite_count,
        "case_count": case_count,
        "team_count": team_count,
        "config_count": config_count
    }
