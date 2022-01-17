from scraper.mongo import MongoOperator


def add_issue_count(request):
    return {
        "issue_count": len(MongoOperator().get_latest_record()['record']['issues'])
    }
