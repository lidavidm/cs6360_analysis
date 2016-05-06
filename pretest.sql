USE cs_6360_spring2016;
SELECT
        user_id,action_detail,MIN(client_timestamp)
FROM player_action_log
WHERE game_id=4 AND action_id=5 AND quest_id=-10
GROUP BY user_id;
