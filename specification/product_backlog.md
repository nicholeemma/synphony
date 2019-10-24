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

| Module                                   | Priority | Estimate | Sprint | Action                                                       |
| ---------------------------------------- | -------- | -------- | ------ | ------------------------------------------------------------ |
| Authorization Related                    | P1       | 3        |        | User signup / login                                          |
|                                          | P1       | 3        |        | Get sharable links for studios                               |
|                                          | P1       | 2        |        | Enter a studio using link                                    |
|                                          | P3       | 5        |        | Host’s position can be switched to one of the participants   |
| **Hosting A Studio (Host)**              | P1       | 2        | 1      | Create a new studio and input information<studio name, etc.> |
|                                          | P1       | 3        | 1      | Search songs from search bar                                 |
|                                          | P1       | 2        | 1      | Add songs to the studio                                      |
|                                          | P1       | 2        | 1      | Play/stop/pause/skip/change songs                            |
|                                          | P1       | 2        |        | Close a studio                                               |
|                                          | P2       | 2        |        | <Nice to have> shuffle/Loop/Single loop songs                |
|                                          | P3       | 1        |        | <Nice to have>customise the capacity(max number of participants) of the studio |
|                                          | P3       | 1        |        | <Nice to have>set the lifetime for a studio (e.g. 2 hours)   |
| **Participating a Studio (Participant)** | P1       | 8        |        | participate in a studio and listen to music in synchronization |
| **Studio**                               | P1       | 1        |        | Display list of users in the studio                          |
|                                          | P1       | 1        |        | Display songs added in the studio                            |
|                                          | P1       | 3        |        | "like" a song in a studio                                    |
|                                          | P2       | 5        |        | send real-time comments in studio                            |
|                                          | P3       | 1        |        | <Nice to have> Display lyrics                                |
| **All Users**                            | P2       | 1        |        | Remove liked songs                                           |
|                                          | P1       | 1        |        | View studio history (either as host or as participant)       |