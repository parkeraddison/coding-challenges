-- Parker Addison
-- 2019.07.07

-- MySQL flavor


-- ######################################################################### --
-- Quoted from:
-- https://www.hackerrank.com/challenges/binary-search-tree-1/problem
--
-- You are given a table, BST, containing two columns: N and P, where N
-- represents the value of a node in Binary Tree, and P is the parent of N.
-- Write a query to find the node type of Binary Tree ordered by the value of
-- the node. Output one of the following for each node:
--   Root: If node is root node.
--   Leaf: If node is leaf node.
--   Inner: If node is neither root nor leaf node.
--
-- Sample Intput:   Sample Output:
-- N | P                
-- 1 | 2            1 Leaf
-- 3 | 2            2 Inner
-- 6 | 8            3 Leaf
-- 9 | 8            5 Root
-- 2 | 5            6 Leaf
-- 8 | 5            8 Inner
-- 5 | null         9 Leaf
-- ######################################################################### --


/*
Here's what I'm thinking:

If we join this table with itself, matching right's P to left's N,
then we can easily see which nodes don't have any children because
the joined columns will be null.  These are leaf nodes.

Nodes which have non-null joined columns are inner nodes, and nodes
which have null P are root node(s).

NOTE: Both joined columns must be null for the node to be a leaf.
 The example above doesn't show any nodes with only one child, but
 it'll be good practice to write code to support such an occurrence
 
 Turns out that this is actually pretty easy to account for, since
 leaf nodes in the joined table will only have one row, which exists
 because we're using a left join.  Additionally, inner nodes will
 only have as many rows as they have children.  So, we don't need to
 do much more logic once the join is complete.
*/

SELECT DISTINCT
    BST.N,
    CASE
        WHEN BST.P IS NULL THEN 'Root'
        WHEN bstright.N IS NULL THEN 'Leaf'
        ELSE 'Inner'
    END
FROM
    BST
    LEFT JOIN BST bstright ON BST.N = bstright.P
ORDER BY BST.N;
