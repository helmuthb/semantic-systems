# library 'readr' - 10x faster reading of CSV files
library('readr')
# dplyr
library(dplyr)
# and tidyr
library(tidyr)

# create Data Frame from CSV file
df <- read_csv('projects.csv',
    col_names = c('id', 'url', 'owner_id', 'name', 'description',
                  'language', 'created_at', 'forked_from', 'deleted',
                  'del_time'),
    col_types = 'icicccDiiD',
    na = c('\\N'))

# read in issues
issues <- read_csv('issues.csv',
    col_names = c('id', 'repo_id', 'reported_id', 'assignee_id',
		  'pull_request', 'pull_request_id', 'created_at',
		  'issue_id'),
    col_types = 'iiiiiiDi',
    na = c('\\N'))

# delete all deleted repositories
df <- df[df$deleted == 0,]

# get number of forks
df %>% group_by(forked_from) %>%
  summarize(forks = n()) %>%
  select(id = forked_from, forks) %>%
  filter(forks > 50) %>%
  drop_na() %>%
  arrange(desc(forks))-> forked_repos

# filter all forks
df %>%
  filter(is.na(forked_from)) %>%
  select(id, url, description, language) -> unforked_repos

# merge repositories
df_merged <- inner_join(unforked_repos, forked_repos)

# get number of issues
issues %>% group_by(repo_id) %>%
  summarize(issues = n()) %>%
  select(id = repo_id, issues) %>%
  drop_na() -> issue_counts

# merge with repositories
inner_join(df_merged, issue_counts) -> repos_issues

# write Data Frame with URL & counts
write_csv(repos_issues, 'repos_issues.csv')

