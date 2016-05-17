USE cs_6360_spring2016;
SELECT
        quest_id, count(DISTINCT user_id)
FROM player_action_log
WHERE game_id = 4 AND log_timestamp >= unix_timestamp('2016-05-09')
GROUP BY quest_id;
