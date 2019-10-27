# Product Backlog

A complete list of all functionality (i.e., the actions) of your project, and an English description of each action. This is your product backlog. We strongly suggest that you organize these features into groups/modules based on related functionality. For each action (or group/module), clearly specify which team member(s) are primarily responsible for the success of that action (or group/module). 



*All pieces of music are called "songs"*

# Functionalities

## Authentication/Authorization Related

* User signup / login
* Generate sharable links for studios
* Enter a studio using link
* <Nice to have>Host’s position can be switched to one of the participants 

## Hosting a Studio

* Hosts create a new studio and input information<studio name, etc.>
* Hosts search songs from search bar 
* Hosts can add songs to the studio
  * From search bar
  * From liked songs
* Hosts play/stop/pause/skip/change songs
* Hosts can close a studio
* <Nice to have> Hosts shuffle/Loop/Single loop songs
* <Nice to have>Hosts can customise the capacity(max number of participants) of the studio 
* <Nice to have>Hosts can set the lifetime for a studio (e.g. 2 hours) 

## Participating a Studio

* P1 Participants can participate in a studio and listen to music in synchronization

## Studio

1. Display list of users in the studio
2. Display songs added in the studio
3. Users can "like" a song in a studio
4. **P2** Users can send real-time comments in studio
5. <Nice to have> Display lyrics 

## User

* Liked songs management (remove, share)
* View studio history (either as host or as participant)

# Todo list

| Module                                   | Priority | Estimate | Sprint | Action                                                       |                                                        | Assigned to |
| ---------------------------------------- | -------- | -------- | ------ | ------------------------------------------------------------ |  ---------- |  ---------- |
| Authorization Related                    | P1       | 2       | 1 | User signup / login                                          | Home page                                 | Alan  |
|                                          | P1       | 3        | 1 | Get sharable links for studios                               | Studio Page                    | Suqi |
|                                          | P1       | 2        | 1 | Enter a studio using link                                    | Home page                           | Suqi |
|                                          | P3       | 5        | - | Host’s position can be switched to one of the participants   |    | Jiayue      |
| **Hosting A Studio (Host)**              | P1       | 2        | 1      | Create a new studio and input information<studio name, etc.> | Creation Page | Alan  |
|                                          | P1       | 3        | 1      | **Search songs from search bar**                             | Studio Page                | W&N |
|                                          | P1       | 2        | 1     | **Add songs to the studio**                                  | Studio Page                           | W&N     |
|                                          | P1       | 2        | 1     | **Play/stop/pause/skip/change songs**                        | Studio Page                 | W&N     |
|                                          | P1       | 2        | 1 | Close a studio                                     | Studio Page                                    | Alan |
|                                          | P2       | 2        | 1 | <Nice to have> shuffle/Loop/Single loop songs                | Studio Page     | -       |
|                                          | P3       | 1        | - | <Nice to have>customise the capacity(max number of participants) of the studio |  |  Alan        |
|                                          | P3       | 1        | - | <Nice to have>set the lifetime for a studio (e.g. 2 hours)   |    |  Alan        |
| **Participating a Studio (Participant)** | P1       | 8     |        | participate in a studio and listen to music in synchronization |  |  Alan        |
| **Studio**                               | P1       | 1        |        | Display list of users in the studio                          |                           | Suqi        |
|                                          | P1       | 1        |        | Display songs added in the studio                            |                             |  Suqi        |
|                                          | P1       | 2       | 1 | "like" a song in a studio                                    | Studio Page                         |  Suqi    |
|                                          | P2       | 5        |        | send real-time comments in studio                            |                             |  Suqi        |
|                                          | P3       | 1        | - | <Nice to have> Display lyrics                                |                                 |  Suqi        |
| **All Users**                            | P2       | 1        |        | Remove liked songs                                           |                                            | Jiayue      |
|                                          | P1       | 1        |        | View studio history (either as host or as participant)       | History Page | Wenjing     |