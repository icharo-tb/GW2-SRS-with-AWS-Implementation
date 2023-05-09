SELECT DISTINCT
	boss_id,
	bosses.boss,
	profession_id,
	profession.professions,
	SUM(profession_id) OVER (PARTITION BY boss_id) AS Total_Profession_Usage,
	ROUND(profession_id * 1.0 / SUM(profession_id) OVER (PARTITION BY boss_id) * 100,4) AS Profession_Usage_Percentage
FROM player_info JOIN profession JOIN bosses ON player_info.boss_id = bosses.id AND player_info.profession_id = profession.id
ORDER BY profession_id ASC;