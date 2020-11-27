Feature: Adding system user

  Scenario: Adding user
    Given the user id isnt taken
     When the user has added a user and account
     Then the id should be placed in the users table with balance 100
