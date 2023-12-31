--- reg fees
select countryId, avg(round(base_entry_fee_lowest_denomination/100,2)) as fee, currency_code as currency 
    from Competitions where countryId in (select distinct countryId 
    from Competitions 
    join Countries on Countries.name = Competitions.countryId 
    where Countries.continentId = "_Europe") and extract(year from start_date) = 2023
    group by countryId order by fee asc

--- rounds per event in germany (past)
select p.event, sum(p.rounds) as rounds from (select eventId as event, count(distinct roundTypeId) as rounds 
    from Results r 
    join Competitions c on r.competitionId = c.id where c.countryId = 'Germany' and extract(year from c.start_date) = 2023 
    group by eventId, competitionId)p 
    group by p.Event order by rounds desc

--- rounds per event in germany (planed)
select ce.event_id as event, count(r.number) as rounds 
    from rounds r 
    join competition_events ce on ce.id = r.competition_event_id 
    join Competitions c on c.id = ce.competition_id where c.countryId = 'Germany' and current_timestamp < c.start_date 
    group by ce.event_id order by rounds desc

--- comps in germany delegated 2023
SELECT delegated_count, person.name
    FROM (
        SELECT COUNT(DISTINCT competition_id) delegated_count, delegate_id
            FROM competition_delegates
            JOIN Competitions competition ON competition.id = competition_id
            WHERE showAtAll = 1 AND cancelled_at IS NULL AND start_date < CURDATE() AND YEAR(start_date) = 2023 AND countryId = "Germany"
            GROUP BY delegate_id
      ) AS delegated_count_by_user
      JOIN users user ON user.id = delegate_id
      JOIN Persons person ON person.wca_id = user.wca_id AND person.subId = 1 
ORDER BY delegated_count DESC

--- comps in germany delegated general
SELECT delegated_count, person.name
    FROM (
        SELECT COUNT(DISTINCT competition_id) delegated_count, delegate_id
            FROM competition_delegates
            JOIN Competitions competition ON competition.id = competition_id
            WHERE showAtAll = 1 AND cancelled_at IS NULL AND start_date < CURDATE() AND countryId = "Germany"
            GROUP BY delegate_id
      ) AS delegated_count_by_user
      JOIN users user ON user.id = delegate_id
      JOIN Persons person ON person.wca_id = user.wca_id AND person.subId = 1 
ORDER BY delegated_count DESC

--- average number of delegates on german comps 2023
select avg(delegates)
    from (
        select count(cd.delegate_id) as delegates 
            from competition_delegates cd 
            join Competitions c on c.id = cd.competition_id 
            where c.countryId="Germany" and year(c.start_date) = 2023 group by cd.competition_id
            ) nested;

--- average orga team size
select avg(orgasum) from (
    select count(cd.organizer_id) as orgasum 
    from competition_organizers cd 
    join Competitions c on c.id = cd.competition_id 
    where c.countryId="Germany" and year(c.start_date) = 2023 group by cd.competition_id
    ) nested;

--- most comps in germany organized
SELECT orga_count, person.name
    FROM (
        SELECT COUNT(DISTINCT competition_id) orga_count, organizer_id
            FROM competition_organizers
            JOIN Competitions competition ON competition.id = competition_id
            WHERE showAtAll = 1 AND cancelled_at IS NULL AND start_date < CURDATE() AND YEAR(start_date) = 2023 AND countryId = "Germany"
            GROUP BY organizer_id
      ) AS delegated_count_by_user
      JOIN users user ON user.id = organizer_id
      JOIN Persons person ON person.wca_id = user.wca_id AND person.subId = 1 
ORDER BY orga_count DESC

--- most comps organized not delegate 2023
SELECT orga_count, person.name
    FROM (
        SELECT COUNT(DISTINCT competition_id) orga_count, organizer_id
            FROM competition_organizers
            JOIN Competitions competition ON competition.id = competition_id
            WHERE showAtAll = 1 AND cancelled_at IS NULL AND start_date < CURDATE() AND YEAR(start_date) = 2023 AND countryId = "Germany"
            GROUP BY organizer_id
      ) AS delegated_count_by_user
      JOIN users user ON user.id = organizer_id
      JOIN Persons person ON person.wca_id = user.wca_id AND person.subId = 1 
where user.delegate_status is null 
ORDER BY orga_count DESC

--- most comps in germany organized general
SELECT orga_count, person.name
    FROM (
        SELECT COUNT(DISTINCT competition_id) orga_count, organizer_id
            FROM competition_organizers
            JOIN Competitions competition ON competition.id = competition_id
            WHERE showAtAll = 1 AND cancelled_at IS NULL AND start_date < CURDATE() AND countryId = "Germany"
            GROUP BY organizer_id
      ) AS delegated_count_by_user
      JOIN users user ON user.id = organizer_id
      JOIN Persons person ON person.wca_id = user.wca_id AND person.subId = 1 
ORDER BY orga_count DESC

--- most comps organized not delegate general
SELECT orga_count, person.name
    FROM (
        SELECT COUNT(DISTINCT competition_id) orga_count, organizer_id
            FROM competition_organizers
            JOIN Competitions competition ON competition.id = competition_id
            WHERE showAtAll = 1 AND cancelled_at IS NULL AND start_date < CURDATE() AND countryId = "Germany"
            GROUP BY organizer_id
      ) AS delegated_count_by_user
      JOIN users user ON user.id = organizer_id
      JOIN Persons person ON person.wca_id = user.wca_id AND person.subId = 1 
where user.delegate_status is null 
ORDER BY orga_count DESC

--- comp duration
select avg(datediff(end_date, start_date)) from Competitions where countryId = "Germany" and year(start_date) = 2023;

--- average number of events
select avg(num_events) from (
    select count(distinct ce.event_id) as num_events 
    from competition_events ce 
    join Competitions c on c.id = ce.competition_id 
    where c.countryId = "Germany" and year(c.start_date) = 2023 group by ce.competition_id
    ) nested;

--- average number of rounds per comp (2023)
select avg(rounds) from(
    select count(ce.event_id) rounds 
    from competition_events ce 
    join rounds r on r.competition_event_id = ce.id 
    join Competitions c on c.id = ce.competition_id 
    where c.countryId = "Germany" and year(c.start_date) = 2023
    group by ce.competition_id
    ) nested;

--- number of rounds per comp
select compid, rounds from(
    select count(ce.event_id) rounds, c.id compid
    from competition_events ce 
    join rounds r on r.competition_event_id = ce.id 
    join Competitions c on c.id = ce.competition_id 
    where c.countryId = "Germany" and year(c.start_date) = 2023
    group by ce.competition_id
    ) nested order by rounds desc

--- comps events, rounds, num comps
select p.event, sum(p.rounds) total_rounds, sum(p.comps) comps_with_event, sum(p.rounds)/c.comps rounds_over_all_comps, sum(p.rounds)/sum(p.comps) rounds_over_held_comps from (select eventId as event, count(distinct roundTypeId) as rounds, count(distinct competitionId) as comps
    from Results r 
    join Competitions c on r.competitionId = c.id where c.countryId = 'Germany' and extract(year from c.start_date) = 2023 
    group by eventId, competitionId)p, (select count(distinct id) as comps from Competitions where countryId = "Germany" and extract(year from start_date) = 2023)c
    group by p.Event order by rounds_over_all_comps desc

--- reg fees per year
select avg(round(base_entry_fee_lowest_denomination/100,2)) as fee, extract(year from start_date) as year
    from Competitions where countryId = "Germany" 
    and extract(year from start_date) in (
        select distinct extract(year from start_date) from Competitions 
        where countryId = "Germany" and extract(year from start_date) > 2016) 
    group by year order by year 

--- been on most german comps general
SELECT competitions, person.name
    FROM (
        SELECT
        COUNT(DISTINCT competitionId) competitions, personId wca_id
        FROM Results result
        JOIN Competitions competition ON competition.id = competitionId
        where competition.countryId = "Germany"
        GROUP BY personId
      ) 
      AS data_by_person
      JOIN Persons person ON person.wca_id = data_by_person.wca_id
      ORDER BY competitions DESC

--- been to most german comps 2023
SELECT competitions, person.name
    FROM (
        SELECT
        COUNT(DISTINCT competitionId) competitions, personId wca_id
        FROM Results result
        JOIN Competitions competition ON competition.id = competitionId
        where competition.countryId = "Germany" and extract(year from competition.start_date) = 2023
        GROUP BY personId
      ) 
      AS data_by_person
      JOIN Persons person ON person.wca_id = data_by_person.wca_id
      ORDER BY competitions DESC

--- german person been to most comps
SELECT competitions, person.name
    FROM (
        SELECT
        COUNT(DISTINCT competitionId) competitions, personId wca_id
        FROM Results result
        JOIN Competitions competition ON competition.id = competitionId
        where extract(year from competition.start_date) = 2023
        GROUP BY personId
    ) 
    AS data_by_person
    JOIN Persons person ON person.wca_id = data_by_person.wca_id
    where person.countryId = "Germany" 
    ORDER BY competitions DESC

--- been to most german comps per year
SELECT (competitions / years) competitions_per_year, competitions, years, person.name
    FROM (
        SELECT
        COUNT(DISTINCT competitionId) competitions,
        (DATEDIFF(CURDATE(), MIN(start_date)) / 365.25) years,
        personId wca_id
        FROM Results result
        JOIN Competitions competition ON competition.id = competitionId
        where competition.countryId = "Germany"
        GROUP BY personId
        HAVING years >= 1
    ) AS data_by_person
    JOIN Persons person ON person.wca_id = data_by_person.wca_id
    ORDER BY competitions_per_year DESC

--- comps per year germans
SELECT (competitions / years) cpy, competitions, years, person.name
    FROM (
        SELECT
        COUNT(DISTINCT competitionId) competitions,
        (DATEDIFF(CURDATE(), MIN(start_date)) / 365.25) years,
        personId wca_id
        FROM Results result
        JOIN Competitions competition ON competition.id = competitionId
        GROUP BY personId
        HAVING years >= 1
    ) AS data_by_person
    JOIN Persons person ON person.wca_id = data_by_person.wca_id
    where person.countryId = "Germany"
    ORDER BY cpy DESC
    LIMIT 21
    