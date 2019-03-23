The Excel Spreadsheet "Survey Data Analysis" is intended to be written too with results from our Google survey.

The spreadsheet produces 5 line graphs. Each line graph has an x-axis which represents the test iteration, or
user test number. The y-axis for each graph represents the number of minutes taken to complete each task (the
task is indicated in each graph title).

These line graphs are intended to demonstrate that as we made changes between testers, there was an overall trend
of tasks being completed more quickly. In other words, the changes we made given the feedback of our previous user
tests made it easier for future users to figure out.

The spreadsheet requires 5 inputs from the survey for each survey response:
1. The time taken to setup GitUp
2. The time taken to backup a local project using GitUp
3. The time taken to add a remote project already backed up using GitUp
4. The time taken to view and compare past versions of files using GitUp
5. The time taken to revert a file to a previous version using GitUp

The spreadsheet can dynamically change it's graphs given increasing amounts of data using Excel's Table feature.
Each input column is an excel table in this spreadsheet. Adding cell values to the end of the table will automatically 
be absorbed into the table and incorporated into the graphs. However, adding data rows through copy and pasting will 
NOT force the tables to absorb the new values below them. If you do copy and paste rows of data though, all you need to
do is drag each of the table bounds down to cover the new data and the graphs will automatically update.
