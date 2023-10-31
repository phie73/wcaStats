--- reg fees
avg(round(base_entry_fee_lowest_denomination/100,2)) as fee, currency_code as currency 
    from Competitions where countryId in (select distinct countryId 
    from Competitions 
    join Countries on Countries.name = Competitions.countryId 
    where Countries.continentId = "_Europe") and extract(year from start_date) = 2022  
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