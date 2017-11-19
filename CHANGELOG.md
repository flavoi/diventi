# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [Unreleased] → xxxx-xx-xx

### Added
- Added profile section on the landing page with a link to the blog page
- Added creation and modification date in blog admin page
- Added admin action to publish articles
- Added a sign up form on the landing page that redirects to the main sign up page

### Changed
- Avatars are now rendered as urls and uploaded in imgur
- Optimized profile page layout for tables
- Improved responsiveness of the timeline
- Blog's articles pub date is now a datetime field to improve the ordering in blogpost page
- Replaced alien fire of the blog list page with a fire icon

### Fixed
- Fixed a problem that caused the cov image to disappear
- Fixed user role in profile page
- Fixed a problem that caused the avatar to not be displayed in article page
- Fixed a problem that caused the avatar to not be displayed in comment section
- Fixed a problem that made the background image of blogposts disappear


## [0.4.2] → 2017-11-08

### Added
- Introduced avatar grouping to better distinguish those reserved to staff members
- Introduced an animated storyline in the landing page to display a list of main events ordered by date
- Introduced the option to show or hide a staff user on the landing page

### Changed
- Avatar is now optional for user sign-up
- Updated media upload folders to better reflect the app names 
- Reorganized profile page with profile and avatar pillows
- Enabled rich text for page elements
- Updated the description of the storyline section

## Fixed
- Fixed a problem in accounts/widgets that caused an error while migrating the database


## [0.3.3] → 2017-10-29

### Added
- Introduced profile page with avatar, bio and favourite class customization options
- Introduced a dedicated profile picture for staff members
- Introduced detailed profile cards into profile update page

### Changed
- Updated name of comment subpage to better reflect its role
- Hard coded role label for every staff member in the landing page
- Restyled icon addon of sign-up recaptcha to improve its responsiveness
- Succes url of signup changed from landing page to login page

### Fixed
- Fixed a problem that caused double comments in comment section
- Fixed a problem that caused the avatar to be hidden in the landing page
- Fixed a problem that caused the sign-up form to fail silently

### Removed
- Removed automatic login after user signup
- Removed new relic monitoring


## [0.2.1] → 2017-10-20

### Added
- Introduced section "comment preview" under the comment post form
- Introduced navigation for the ordering of comments by promotions or submit date
- Introduced comment toggle button to hide/display all comments

### Changed
- Renamed version.txt to CHANGELOG and adopted Keep a Changelog method for versioning
- Updated README with LICENCE, versioning and incipit infos
- Updated cover visuals in blogposts page

### Fixed
- Fixed a problem that caused the avatar to be a requirement for comment post

### Removed
- Removed icons from navbar


## [0.1.0] → 2017-10-14

### Added
- Introduced a landing page with the presentation of our product
- Introduced a simple accounts management system
- Introduced a blog section
- Introduced a commenting system for the articles
- Introduced a sign-up page with username, email and password 
- Introduced a promotions system for articles and comments
- Introduced an author section on the article page
- Introduced a recaptcha field on the sign-up page