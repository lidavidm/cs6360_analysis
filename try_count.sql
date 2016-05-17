USE cs_6360_spring2016;
SELECT quest_id, user_id FROM player_action_log WHERE game_id = 4 AND action_id=3 AND (action_detail LIKE "{\"event\":\"normal\"%" OR action_detail="{\"event\":\"invalid\"}") ORDER BY quest_id, user_id;
