
English | [繁體中文](README.zh-TW.md)

# Discord Admin Bot

This bot is design to manage the discord server automatic. 

You only need to type some simple command and you will have a clearly server. 

It's a very nice robot for someone doesn't understand how to management their server or want to manage your server more easier. 


![Logo](https://download.logo.wine/logo/Discord_(software)/Discord_(software)-Logo.wine.png)


## Screenshots

![App Screenshot](https://media.discordapp.net/attachments/986465905582161970/991900345531904030/unknown.png)


## Features

- Recation role
- Automatic voice channel extend
- Vote
- Random grouping
- Event counter


## Installation

Install python

https://www.python.org/downloads/


Install discord.py with pip

```bash
  pip install discord.py
```

Install emoji with pip

```bash
  pip install emoji
```

Install alive-progress with pip

```bash
  pip install alive-progress
```
## Environment Variables

To run this project, you will need to add the following environment variables to your config.py file

`API_KEY`

## Usage/Examples

After config.py setucompleted open server.bat and you can use this bot on discord.

## Command

### instructions

`*('argument' 'argument2')` mean you can repeat this argument groups for many times

`(reply message requier)` mean you need to reply a message and type this command to use it.

You can use custom emoji on your commands

### Recation role

command

```bash
  &reaction_role *('emoji' '@roles') (reply message requier)
```

example

```bash
  &reaction_role :rocket: @role1 :ok_hand: @role2
```

### Vote

command

```bash
  &vote 'question' 'hour' *('option_emoji' 'option_content')
```

example

```bash
  &vote "Saturday or Sunday" 24 *(:ringed_planet: "Saturday" :sunny: "Sunday")
```

### Random grouping

command

```bash
  &random_team *('@mentions or string')
```

example

```bash
  &vote @user1 @user2 @user3 @user4 @user5 @user6
```

### Event counter

command

```bash
  &event_host 'title' 'goal' 'hour'
```

example

```bash
  &event_host "BBQ on sunday lunch" 10 48
```

## Roadmap

- move data to database

- Add more features

- support english

## Optimizations

- Update readme file 

