-- When do contiguous attack episodes start and end?
WITH x AS (SELECT time,attack,LAG(attack,1,0) OVER (ORDER BY time) previous FROM readings WHERE split='test'), y AS (SELECT *,SUM((attack=1 AND previous=0)::INT) OVER (ORDER BY time) episode FROM x) SELECT episode,MIN(time) start_time,MAX(time) end_time,COUNT(*) duration_seconds FROM y WHERE attack=1 GROUP BY 1 ORDER BY 1;
