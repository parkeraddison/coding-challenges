-- Parker Addison
-- 2019.07.12

-- MySQL flavor


-- ######################################################################### --
-- Quoted/paraphrased from:
-- https://www.hackerrank.com/challenges/interviews/problem
--
-- Samantha interviews many candidates from different colleges using coding
-- challenges and contests.
-- Write a query to print the contest_id, hacker_id, name, and the sums of
-- total_submissions, total_accepted_submissions, total_views, and
-- total_unique_views for each contest sorted by contest_id.
-- Exclude the contest from the result if all four sums are 0.
-- Note: A specific contest can be used to screen candidates at more than one
-- college, but each college only holds 1 screening contest.
--
-- The following tables/columns exist:
--   Contests: contest_id, hacker_id, name.  Where hacker_id and name are of
--   the hacker who set up the contest.
--
--   Colleges: college_id, contest_id
--
--   Challenges: challenge_id, college_id
--
--   View_Stats: challenge_id, total_views, total_unique_views
--
--   Submission_Stats: challenge_id, total_submissions,
--   total_accepted_submissions
--
-- Sample Input:
--! NOTE:See bottom of the file for a schema to build the sample data.
--
-- Sample Output:
-- 66406 17973   Rose 111 39 156 56
-- 66556 79153 Angela   0  0  11 10
-- 94828 80275  Frank 150 38  41 15
-- ######################################################################### --


/*
Here's what I'm thinking...

We'll need the following columns:
 contest_id, hacker_id, name, total_submissions, total_accepted_submissions,
 total_views, total_unique_views

I'm going to start with the Contests table since we want to have a row for each
contest, and we want to have all columns included in Contests.

In order to get the total submissions from  the Submission_Stats table, we'll
need to first get the challenge_id.  To do this, we need to look at colleges.
So, for each contest we'll join with Colleges to get all colleges which used
that particular contest, then we'll simply join those colleges with Challenges
to get all challenges which were part of that particular contest.  Now, once we
have the challenges then we can easily join with Submission_Stats to get total
submissions.

Once all of that joining above has been accomplished, it's as simple as
modifying the final step to get the remaining columns joined in to our table.

Finally, once we have all of the columns and rows for each contest/challenge,
then we can group by the contest id and aggregate the sums of the other fields
as we desire.

--

Ran into an issue.  When a join happens on View_Stats or Submission_Stats then
duplicate contest_id rows come into existence to accomodate for duplicate
challenge_id rows in the Stats tables.

To fix this, we should aggregate the Stats tables before joining.

See below for better explanation of this problem/solution.
*/


SELECT
    Contests.*
    -- The following lines were for debugging
    -- ,Colleges.college_id
    -- ,Challenges.challenge_id
    -- ,SubStats.*
    -- ,ViewStats.*
    -- The IFNULL is necessary to output zeros instead of null!
    ,IFNULL(SUM(SubStats.total_submissions), 0)
    ,IFNULL(SUM(SubStats.total_accepted_submissions), 0)
    ,IFNULL(SUM(ViewStats.total_views), 0)
    ,IFNULL(SUM(ViewStats.total_unique_views), 0)

FROM
    Contests
    
    -- The first steps are easy.  We just need to do a couple joins in order to
    -- move from contest_id to corresponding challenge_id(s)
    INNER JOIN Colleges ON Contests.contest_id = Colleges.contest_id
    INNER JOIN Challenges ON Colleges.college_id = Challenges.college_id
    
    -- Here's where things get a bit trickier.  As brainstormed above, solely a
    -- left join with the View_Stats table will actually end up producing
    -- duplicate rows of contest_id.  Next, when we want to join with the
    -- Submission_Stats table then we're stuck with a many-to-many situation!
    -- (yikes)
    -- This is because the Stats tables can contain multiple rows for the same
    -- challenge_id.  This situation can be noted in the sample data provided.
    -- 
    -- If we aggregate on challenge_id within each Stat table first then we can
    -- avoid the problem of many-to-many joins.
    LEFT JOIN (
      SELECT
        challenge_id
        ,SUM(total_views) as total_views
        ,SUM(total_unique_views) as total_unique_views
      FROM View_Stats
      GROUP BY challenge_id
    ) AS ViewStats ON Challenges.challenge_id = ViewStats.challenge_id
    
    LEFT JOIN (
      SELECT
        challenge_id
        ,SUM(total_submissions) as total_submissions
        ,SUM(total_accepted_submissions) as total_accepted_submissions
      FROM Submission_Stats
      GROUP BY challenge_id
    ) AS SubStats ON Challenges.challenge_id = SubStats.challenge_id
    
-- Finally, we can group/aggregate on all of the fields unique to a contest.
GROUP BY
    contest_id, hacker_id, name

-- And the problem asks us to exclude rows with all four sums being zeros.
--
-- Note that we need to use HAVING rather than WHERE because we're accessing
-- group data.
HAVING
    SUM(total_views) > 0
    OR SUM(total_unique_views) > 0
    OR SUM(total_submissions) > 0
    OR SUM(total_accepted_submissions) > 0

ORDER BY
    contest_id
;

-- ######################################################################### --
-- Schema of sample data:
/*
CREATE TABLE Contests (
    contest_id INT
    ,hacker_id INT
    ,name VARCHAR(8)
);

INSERT INTO Contests
    (contest_id, hacker_id, name)
VALUES
    (66406, 17973, "Rose"), (66556, 79153, "Angela"), (94828, 80275, "Frank")
;

CREATE TABLE Colleges (
    college_id INT
    ,contest_id INT
);

INSERT INTO Colleges
    (college_id, contest_id)
VALUES
    (11219, 66406), (32473, 66556), (56685, 94828)
;

CREATE TABLE Challenges (
    challenge_id INT
    ,college_id INT
);

INSERT INTO Challenges
    (challenge_id, college_id)
VALUES
    (18765, 11219), (47127, 11219), (60292, 32473), (72974, 56685)
;

CREATE TABLE View_Stats (
    challenge_id INT
    ,total_views INT
    ,total_unique_views INT
);

INSERT INTO View_Stats
    (challenge_id, total_views, total_unique_views)
VALUES
    (47127, 26, 19), (47127, 15, 14), (18765, 43, 10), (18765, 72, 13),
    (75516, 35, 17), (60292, 11, 10), (72974, 41, 15), (75516, 75, 11)
;

CREATE TABLE Submission_Stats (
    challenge_id INT
    ,total_submissions INT
    ,total_unique_submissions INT
);

INSERT INTO Submission_Stats
    (challenge_id, total_submissions, total_unique_submissions)
VALUES
    (75516, 34, 12), (47127, 27, 10), (47127, 56, 18), (75516, 74, 12),
    (75516, 83, 8), (72974, 68, 24), (72974, 82, 14), (47127, 28, 11)
;
*/