-- (id, name, wins, matches):
    select  id, name, coalesce( W.wins, 0) as wins, matches
    from
        players p left join
        ( select winner, count(winner) as wins from matches group by winner) as W
        on id=W.winner
    group by (id, w.wins)
    order by id desc
    ;
