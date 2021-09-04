Feature: Dzirkstele and gulbene

Scenario: run a simple test
  Given launch "gulbene" page
  When I read data
  And store data
  And send email

  Scenario: run a simple test
  Given launch "dzirkstele" page
  When I read data
  And store data
  And send email