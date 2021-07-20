-- FIRST QUERY

insert into all_users (id, first_name, last_name, phone_number, zip_code, month_registered)
select 
--Since there are no people in the all_users table yet, we can start from 1
  row_number() over(order by last_first_name) as id
-- Seperate first and last name and make it all upper case just for standardizing.
  , upper(trim(SPLIT_PART(last_first_name, ',',2))) as first_name
  , upper(trim(SPLIT_PART(last_first_name, ',',1))) as last_name
-- Make the phone numbers numbers only. IRL I would consider if they all have the same number of digits or some are missing 1.
  , NULLIF(regexp_replace(phone, '\D','','g'), '')::numeric as phone_number
--Zipcodes should all be at least 5 digits. Assuming that those fewer than 5 were misinterpreted because they began with 0's.
  , (case when length(zip_code)=3 then concat(0, 0,zip_code)
      when length(zip_code)=4 then concat(0,zip_code)
      else zip_code end
  ) as zip_code
-- Getting year and month for month registered in a format that is text but, if sorted, would sort by time.
  , concat(extract(year from reg_date), '-'
      , (case when length(cast(extract(month from reg_date) as text))=1 then concat(0, cast(extract(month from reg_date) as text))
          when length(cast(extract(month from reg_date) as text))=2 then cast(extract(month from reg_date) as text)
          else null end)
    ) as month_registered
from vendor4_users
where 
--Assuming if a user were correctly registered that they would have a zipcode AND that we want valid registrations in all_users
  is_valid_registration is true and zip_code is not null
;


-- SEOCOND QUERY

--Total regsistrations, completed registrations, valid incomplete registrations
-- by organization and state
select org, state
  , count(*) as total
  , count(case when is_complete_registration is true then 1 else null end) as completed_registrations
  , count(case when is_valid_registration is true and is_complete_registration is false then 1 else null end) as valid_incomplete_registrations
from registrations
group by org, state
order by total desc
;


-- THURD QUERY

--Create a subquery to group
with detailed_dials as (select p.name as program_name
  , p.date as program_date
  --Replaceing autodialer for where caller is not known (caller_id is null since there are no cases where this is true and name is not null)
  , (case when c.id is null then 'autodialer' else c.name end) as caller_name
from dials as d
full join callers as c on c.id = d.caller_id
full join programs as p on p.id = d.program_id
--Assuming we don't want program id to be null.
where p.id is not null)

--Get counts per person on a given date in a given program.
select program_name, program_date
  , caller_name
  , count(*) as num_calls
from detailed_dials
group by 1,2,3
order by program_date asc, num_calls desc
;
