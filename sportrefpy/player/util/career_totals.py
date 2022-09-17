from typing import Dict
from typing import List


class CareerTotals:
    @staticmethod
    def unpack_career_stats(
        regular_season, post_season, stats_to_include: List, totals: Dict
    ):
        for seasons in [regular_season, post_season]:
            for _, season in seasons.items():
                for stat, value in season.items():
                    if stat in stats_to_include:
                        if stat not in totals:
                            totals[stat] = value
                        elif not value:
                            continue
                        else:
                            totals[stat] += value
        return totals
