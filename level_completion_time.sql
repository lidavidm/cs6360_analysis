USE cs_6360_spring2016;
SELECT
        quest_id, user_id, level_end_timestamp - log_quest_ts
FROM player_quest_log
WHERE
        level_end_timestamp IS NOT NULL AND
        game_id = 4 AND
        user_id in (
                SELECT
                        user_id
                FROM player_action_log
                WHERE
                        game_id = 4 AND
                        quest_id = -20 AND
                        log_timestamp >= unix_timestamp('2016-05-09')
                )
GROUP BY quest_id,user_id;
