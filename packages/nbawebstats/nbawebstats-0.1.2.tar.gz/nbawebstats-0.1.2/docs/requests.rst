====================
Request Reference
====================

********
Requests
********

.. _request-all-games:

all-games
-------------------------------


Required Parameters:
  :ref:`Season <param-season>`

Optional Parameters:
  :ref:`Direction <param-direction>`, :ref:`LeagueID <param-leagueid>`, :ref:`PlayerOrTeam <param-playerorteam>`, :ref:`SeasonType <param-seasontype>`, :ref:`Sorter <param-sorter>`

Return Fields:
  ``'list'``
    ``'BLK'``, ``'PTS'``, ``'VIDEO_AVAILABLE'``, ``'FTM'``, ``'WL'``, ``'FG_PCT'``, ``'SEASON_ID'``, ``'TEAM_ABBREVIATION'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'DREB'``, ``'FG3M'``, ``'AST'``, ``'PF'``, ``'GAME_ID'``, ``'FG3_PCT'``, ``'OREB'``, ``'TEAM_NAME'``, ``'FG3A'``, ``'GAME_DATE'``, ``'TOV'``, ``'TEAM_ID'``, ``'PLUS_MINUS'``

    

.. _request-all-players:

all-players
-------------------------------


Required Parameters:
  :ref:`Season <param-season>`

Optional Parameters:
  :ref:`IsOnlyCurrentSeason <param-isonlycurrentseason>`, :ref:`LeagueID <param-leagueid>`

Return Fields:
  ``'list'``
    ``'PLAYERCODE'``, ``'GAMES_PLAYED_FLAG'``, ``'DISPLAY_FIRST_LAST'``, ``'TEAM_NAME'``, ``'TEAM_ABBREVIATION'``, ``'TO_YEAR'``, ``'PERSON_ID'``, ``'ROSTERSTATUS'``, ``'TEAM_ID'``, ``'TEAM_CITY'``, ``'TEAM_CODE'``

    

.. _request-draft-agility:

draft-agility
-------------------------------


Required Parameters:
  :ref:`SeasonYear <param-seasonyear>`

Optional Parameters:
  :ref:`LeagueID <param-leagueid>`

Return Fields:
  ``'data'``
    ``'LANE_AGILITY_TIME'``, ``'LAST_NAME'``, ``'POSITION'``, ``'FIRST_NAME'``, ``'THREE_QUARTER_SPRINT'``, ``'PLAYER_NAME'``, ``'MODIFIED_LANE_AGILITY_TIME'``, ``'MAX_VERTICAL_LEAP'``, ``'PLAYER_ID'``, ``'BENCH_PRESS'``, ``'STANDING_VERTICAL_LEAP'``

    

.. _request-draft-anthro:

draft-anthro
-------------------------------


Required Parameters:
  :ref:`SeasonYear <param-seasonyear>`

Optional Parameters:
  :ref:`LeagueID <param-leagueid>`

Return Fields:
  ``'data'``
    ``'STANDING_REACH'``, ``'HAND_WIDTH'``, ``'LAST_NAME'``, ``'POSITION'``, ``'FIRST_NAME'``, ``'HEIGHT_W_SHOES_FT_IN'``, ``'HEIGHT_W_SHOES'``, ``'BODY_FAT_PCT'``, ``'HEIGHT_WO_SHOES'``, ``'STANDING_REACH_FT_IN'``, ``'PLAYER_ID'``, ``'PLAYER_NAME'``, ``'WINGSPAN'``, ``'WEIGHT'``, ``'TEMP_PLAYER_ID'``, ``'HEIGHT_WO_SHOES_FT_IN'``, ``'WINGSPAN_FT_IN'``

    

.. _request-draft-combine-all-stats:

draft-combine-all-stats
-------------------------------


Required Parameters:
  :ref:`SeasonYear <param-seasonyear>`

Optional Parameters:
  :ref:`LeagueID <param-leagueid>`

Return Fields:
  ``'data'``
    ``'LANE_AGILITY_TIME'``, ``'LAST_NAME'``, ``'POSITION'``, ``'FIRST_NAME'``, ``'THREE_QUARTER_SPRINT'``, ``'PLAYER_NAME'``, ``'MODIFIED_LANE_AGILITY_TIME'``, ``'MAX_VERTICAL_LEAP'``, ``'PLAYER_ID'``, ``'BENCH_PRESS'``, ``'STANDING_VERTICAL_LEAP'``

    

.. _request-draft-non-stationary-shooting:

draft-non-stationary-shooting
-------------------------------


Required Parameters:
  :ref:`SeasonYear <param-seasonyear>`

Optional Parameters:
  :ref:`LeagueID <param-leagueid>`

Return Fields:
  ``'data'``
    ``'OFF_DRIB_FIFTEEN_BREAK_LEFT_ATTEMPT'``, ``'POSITION'``, ``'ON_MOVE_FIFTEEN_PCT'``, ``'PLAYER_ID'``, ``'OFF_DRIB_COLLEGE_BREAK_LEFT_MADE'``, ``'ON_MOVE_FIFTEEN_ATTEMPT'``, ``'ON_MOVE_COLLEGE_MADE'``, ``'PLAYER_NAME'``, ``'OFF_DRIB_COLLEGE_TOP_KEY_PCT'``, ``'OFF_DRIB_FIFTEEN_BREAK_RIGHT_MADE'``, ``'TEMP_PLAYER_ID'``, ``'OFF_DRIB_FIFTEEN_TOP_KEY_ATTEMPT'``, ``'OFF_DRIB_COLLEGE_BREAK_RIGHT_ATTEMPT'``, ``'OFF_DRIB_FIFTEEN_TOP_KEY_PCT'``, ``'OFF_DRIB_FIFTEEN_BREAK_LEFT_PCT'``, ``'LAST_NAME'``, ``'OFF_DRIB_COLLEGE_BREAK_RIGHT_MADE'``, ``'FIRST_NAME'``, ``'OFF_DRIB_FIFTEEN_BREAK_RIGHT_ATTEMPT'``, ``'OFF_DRIB_COLLEGE_BREAK_LEFT_ATTEMPT'``, ``'OFF_DRIB_COLLEGE_TOP_KEY_MADE'``, ``'ON_MOVE_FIFTEEN_MADE'``, ``'ON_MOVE_COLLEGE_ATTEMPT'``, ``'OFF_DRIB_COLLEGE_BREAK_RIGHT_PCT'``, ``'OFF_DRIB_FIFTEEN_BREAK_LEFT_MADE'``, ``'OFF_DRIB_FIFTEEN_TOP_KEY_MADE'``, ``'OFF_DRIB_COLLEGE_TOP_KEY_ATTEMPT'``, ``'OFF_DRIB_COLLEGE_BREAK_LEFT_PCT'``, ``'ON_MOVE_COLLEGE_PCT'``

    

.. _request-draft-spot-shooting:

draft-spot-shooting
-------------------------------


Required Parameters:
  :ref:`SeasonYear <param-seasonyear>`

Optional Parameters:
  :ref:`LeagueID <param-leagueid>`

Return Fields:
  ``'data'``
    ``'NBA_BREAK_RIGHT_MADE'``, ``'NBA_BREAK_LEFT_MADE'``, ``'NBA_CORNER_LEFT_MADE'``, ``'COLLEGE_TOP_KEY_MADE'``, ``'POSITION'``, ``'NBA_CORNER_RIGHT_ATTEMPT'``, ``'NBA_BREAK_LEFT_PCT'``, ``'COLLEGE_CORNER_RIGHT_PCT'``, ``'NBA_CORNER_LEFT_PCT'``, ``'COLLEGE_CORNER_LEFT_MADE'``, ``'FIFTEEN_CORNER_RIGHT_PCT'``, ``'FIFTEEN_CORNER_RIGHT_ATTEMPT'``, ``'COLLEGE_BREAK_RIGHT_ATTEMPT'``, ``'FIFTEEN_TOP_KEY_MADE'``, ``'NBA_CORNER_RIGHT_MADE'``, ``'FIFTEEN_CORNER_RIGHT_MADE'``, ``'COLLEGE_TOP_KEY_PCT'``, ``'FIFTEEN_CORNER_LEFT_MADE'``, ``'NBA_BREAK_LEFT_ATTEMPT'``, ``'FIFTEEN_TOP_KEY_PCT'``, ``'COLLEGE_CORNER_RIGHT_MADE'``, ``'COLLEGE_CORNER_LEFT_ATTEMPT'``, ``'FIFTEEN_BREAK_LEFT_PCT'``, ``'NBA_TOP_KEY_MADE'``, ``'PLAYER_ID'``, ``'COLLEGE_CORNER_RIGHT_ATTEMPT'``, ``'COLLEGE_BREAK_RIGHT_MADE'``, ``'NBA_BREAK_RIGHT_PCT'``, ``'TEMP_PLAYER_ID'``, ``'NBA_CORNER_LEFT_ATTEMPT'``, ``'NBA_TOP_KEY_ATTEMPT'``, ``'COLLEGE_TOP_KEY_ATTEMPT'``, ``'NBA_BREAK_RIGHT_ATTEMPT'``, ``'FIFTEEN_BREAK_LEFT_ATTEMPT'``, ``'FIFTEEN_CORNER_LEFT_ATTEMPT'``, ``'NBA_TOP_KEY_PCT'``, ``'COLLEGE_CORNER_LEFT_PCT'``, ``'COLLEGE_BREAK_LEFT_MADE'``, ``'COLLEGE_BREAK_LEFT_PCT'``, ``'LAST_NAME'``, ``'NBA_CORNER_RIGHT_PCT'``, ``'COLLEGE_BREAK_RIGHT_PCT'``, ``'PLAYER_NAME'``, ``'FIFTEEN_TOP_KEY_ATTEMPT'``, ``'FIFTEEN_BREAK_RIGHT_PCT'``, ``'FIFTEEN_CORNER_LEFT_PCT'``, ``'FIFTEEN_BREAK_LEFT_MADE'``, ``'COLLEGE_BREAK_LEFT_ATTEMPT'``, ``'FIFTEEN_BREAK_RIGHT_ATTEMPT'``

    

.. _request-game-boxscore-advanced:

game-boxscore-advanced
-------------------------------


Required Parameters:
  :ref:`GameID <param-gameid>`

Optional Parameters:
  :ref:`EndPeriod <param-endperiod>`, :ref:`EndRange <param-endrange>`, :ref:`RangeType <param-rangetype>`, :ref:`StartPeriod <param-startperiod>`, :ref:`StartRange <param-startrange>`

Return Fields:
  ``'player-stats'``
    ``'USG_PCT'``, ``'AST_TOV'``, ``'TEAM_ABBREVIATION'``, ``'OFF_RATING'``, ``'AST_PCT'``, ``'DREB_PCT'``, ``'EFG_PCT'``, ``'TEAM_CITY'``, ``'START_POSITION'``, ``'PLAYER_ID'``, ``'PIE'``, ``'COMMENT'``, ``'PACE'``, ``'NET_RATING'``, ``'AST_RATIO'``, ``'PLAYER_NAME'``, ``'TS_PCT'``, ``'GAME_ID'``, ``'REB_PCT'``, ``'TEAM_ID'``, ``'OREB_PCT'``, ``'MIN'``, ``'TM_TOV_PCT'``

  ``'team-stats'``
    ``'TEAM_ID'``, ``'AST_PCT'``, ``'NET_RATING'``, ``'DREB_PCT'``, ``'AST_TOV'``, ``'AST_RATIO'``, ``'TEAM_ABBREVIATION'``, ``'TEAM_NAME'``, ``'OFF_RATING'``, ``'TS_PCT'``, ``'GAME_ID'``, ``'REB_PCT'``, ``'EFG_PCT'``, ``'TEAM_CITY'``, ``'OREB_PCT'``, ``'MIN'``

    

.. _request-game-boxscore-fourfactors:

game-boxscore-fourfactors
-------------------------------


Required Parameters:
  :ref:`GameID <param-gameid>`

Optional Parameters:
  :ref:`EndPeriod <param-endperiod>`, :ref:`EndRange <param-endrange>`, :ref:`RangeType <param-rangetype>`, :ref:`StartPeriod <param-startperiod>`, :ref:`StartRange <param-startrange>`

Return Fields:
  ``'player-stats'``
    ``'FTA_RATE'``, ``'PLAYER_ID'``, ``'OPP_FTA_RATE'``, ``'TEAM_ABBREVIATION'``, ``'PLAYER_NAME'``, ``'GAME_ID'``, ``'OPP_TOV_PCT'``, ``'OPP_OREB_PCT'``, ``'EFG_PCT'``, ``'TEAM_CITY'``, ``'OREB_PCT'``, ``'MIN'``, ``'START_POSITION'``, ``'TM_TOV_PCT'``

  ``'team-stats'``
    ``'FTA_RATE'``, ``'TEAM_ABBREVIATION'``, ``'TEAM_NAME'``, ``'GAME_ID'``, ``'OPP_TOV_PCT'``, ``'OPP_OREB_PCT'``, ``'EFG_PCT'``, ``'TEAM_CITY'``, ``'OREB_PCT'``, ``'MIN'``, ``'TM_TOV_PCT'``

    

.. _request-game-boxscore-misc:

game-boxscore-misc
-------------------------------


Required Parameters:
  :ref:`GameID <param-gameid>`

Optional Parameters:
  :ref:`EndPeriod <param-endperiod>`, :ref:`EndRange <param-endrange>`, :ref:`RangeType <param-rangetype>`, :ref:`StartPeriod <param-startperiod>`, :ref:`StartRange <param-startrange>`

Return Fields:
  ``'player-stats'``
    ``'TEAM_ID'``, ``'GAME_ID'``, ``'BLK'``, ``'OPP_PTS_2ND_CHANCE'``, ``'PTS_FB'``, ``'OPP_PTS_OFF_TOV'``, ``'PFD'``, ``'PLAYER_ID'``, ``'PTS_PAINT'``, ``'TEAM_ABBREVIATION'``, ``'PLAYER_NAME'``, ``'PTS_OFF_TOV'``, ``'PF'``, ``'COMMENT'``, ``'TEAM_CITY'``, ``'OPP_PTS_PAINT'``, ``'OPP_PTS_FB'``, ``'START_POSITION'``

  ``'team-stats'``
    ``'GAME_ID'``, ``'BLK'``, ``'OPP_PTS_PAINT'``, ``'PTS_FB'``, ``'PFD'``, ``'PTS_PAINT'``, ``'TEAM_ABBREVIATION'``, ``'TEAM_NAME'``, ``'PTS_2ND_CHANCE'``, ``'PTS_OFF_TOV'``, ``'PF'``, ``'TEAM_ID'``, ``'TEAM_CITY'``, ``'MIN'``, ``'OPP_PTS_FB'``

    

.. _request-game-boxscore-scoring:

game-boxscore-scoring
-------------------------------


Required Parameters:
  :ref:`GameID <param-gameid>`

Optional Parameters:
  :ref:`EndPeriod <param-endperiod>`, :ref:`EndRange <param-endrange>`, :ref:`RangeType <param-rangetype>`, :ref:`StartPeriod <param-startperiod>`, :ref:`StartRange <param-startrange>`

Return Fields:
  ``'player-stats'``
    ``'PCT_AST_3PM'``, ``'PCT_FGA_3PT'``, ``'PCT_PTS_2PT'``, ``'PCT_PTS_FB'``, ``'TEAM_ABBREVIATION'``, ``'PCT_UAST_FGM'``, ``'PCT_PTS_FT'``, ``'COMMENT'``, ``'TEAM_CITY'``, ``'PCT_FGA_2PT'``, ``'MIN'``, ``'PCT_AST_FGM'``, ``'START_POSITION'``, ``'PCT_PTS_3PT'``, ``'PCT_PTS_2PT_MR'``, ``'PCT_PTS_PAINT'``, ``'PCT_PTS_OFF_TOV'``, ``'PCT_UAST_2PM'``, ``'PLAYER_NAME'``, ``'GAME_ID'``, ``'PLAYER_ID'``

  ``'team-stats'``
    ``'PCT_AST_3PM'``, ``'PCT_PTS_3PT'``, ``'PCT_PTS_2PT_MR'``, ``'PCT_PTS_PAINT'``, ``'PCT_PTS_OFF_TOV'``, ``'PCT_FGA_3PT'``, ``'PCT_PTS_2PT'``, ``'PCT_UAST_FGM'``, ``'PCT_UAST_2PM'``, ``'TEAM_ABBREVIATION'``, ``'PCT_PTS_FB'``, ``'TEAM_NAME'``, ``'GAME_ID'``, ``'PCT_PTS_FT'``, ``'TEAM_ID'``, ``'TEAM_CITY'``, ``'PCT_FGA_2PT'``, ``'MIN'``, ``'PCT_AST_2PM'``, ``'PCT_AST_FGM'``

    

.. _request-game-boxscore-summary:

game-boxscore-summary
-------------------------------


Required Parameters:
  :ref:`GameID <param-gameid>`

Optional Parameters:
  

Return Fields:
  ``'game-summary'``
    ``'GAME_STATUS_TEXT'``, ``'GAME_ID'``, ``'VISITOR_TEAM_ID'``, ``'GAME_SEQUENCE'``, ``'NATL_TV_BROADCASTER_ABBREVIATION'``, ``'GAME_DATE_EST'``, ``'GAME_STATUS_ID'``, ``'WH_STATUS'``, ``'GAMECODE'``, ``'HOME_TEAM_ID'``, ``'LIVE_PC_TIME'``

  ``'other-stats'``
    ``'TIMES_TIED'``, ``'LARGEST_LEAD'``, ``'TEAM_CITY'``, ``'PTS_FB'``, ``'LEAD_CHANGES'``, ``'PTS_PAINT'``, ``'TEAM_ABBREVIATION'``

  ``'officials'``
    ``'LAST_NAME'``, ``'OFFICIAL_ID'``, ``'FIRST_NAME'``

  ``'inactive-players'``
    ``'JERSEY_NUM'``, ``'PLAYER_ID'``, ``'TEAM_CITY'``, ``'LAST_NAME'``, ``'FIRST_NAME'``, ``'TEAM_ABBREVIATION'``, ``'TEAM_NAME'``

  ``'game-info'``
    

  ``'line-score'``
    ``'PTS_OT6'``, ``'PTS_OT7'``, ``'PTS_OT2'``, ``'PTS'``, ``'GAME_DATE_EST'``, ``'PTS_QTR1'``, ``'TEAM_ABBREVIATION'``, ``'PTS_QTR4'``, ``'PTS_QTR3'``, ``'TEAM_WINS_LOSSES'``, ``'PTS_OT5'``, ``'PTS_OT1'``, ``'PTS_OT8'``, ``'PTS_OT3'``, ``'PTS_OT4'``, ``'GAME_SEQUENCE'``, ``'TEAM_NICKNAME'``, ``'PTS_OT9'``, ``'PTS_QTR2'``, ``'TEAM_CITY_NAME'``, ``'GAME_ID'``, ``'TEAM_ID'``

  ``'last-meeting'``
    ``'GAME_ID'``, ``'LAST_GAME_VISITOR_TEAM_ID'``, ``'LAST_GAME_VISITOR_TEAM_CITY'``, ``'LAST_GAME_ID'``, ``'LAST_GAME_HOME_TEAM_CITY'``, ``'LAST_GAME_HOME_TEAM_ID'``, ``'LAST_GAME_HOME_TEAM_POINTS'``, ``'LAST_GAME_VISITOR_TEAM_NAME'``, ``'LAST_GAME_DATE_EST'``, ``'LAST_GAME_HOME_TEAM_ABBREVIATION'``, ``'LAST_GAME_HOME_TEAM_NAME'``, ``'LAST_GAME_VISITOR_TEAM_CITY1'``

  ``'season-series'``
    ``'GAME_ID'``, ``'VISITOR_TEAM_ID'``, ``'HOME_TEAM_LOSSES'``, ``'GAME_DATE_EST'``, ``'SERIES_LEADER'``, ``'HOME_TEAM_WINS'``

  ``'available-video'``
    ``'PT_XYZ_AVAILABLE'``, ``'PT_AVAILABLE'``, ``'GAME_ID'``

    

.. _request-game-boxscore-tracking:

game-boxscore-tracking
-------------------------------


Required Parameters:
  :ref:`GameID <param-gameid>`

Optional Parameters:
  

Return Fields:
  ``'player-stats'``
    

  ``'team-stats'``
    

    

.. _request-game-boxscore-traditional:

game-boxscore-traditional
-------------------------------


Required Parameters:
  :ref:`GameID <param-gameid>`

Optional Parameters:
  :ref:`EndPeriod <param-endperiod>`, :ref:`EndRange <param-endrange>`, :ref:`RangeType <param-rangetype>`, :ref:`StartPeriod <param-startperiod>`, :ref:`StartRange <param-startrange>`

Return Fields:
  ``'player-stats'``
    ``'DFGM'``, ``'DFG_PCT'``, ``'RBC'``, ``'CFGA'``, ``'TCHS'``, ``'TEAM_ABBREVIATION'``, ``'SPD'``, ``'PASS'``, ``'COMMENT'``, ``'TEAM_CITY'``, ``'CFG_PCT'``, ``'START_POSITION'``, ``'DIST'``, ``'FTAST'``, ``'UFG_PCT'``, ``'FG_PCT'``, ``'UFGM'``, ``'AST'``, ``'ORBC'``, ``'SAST'``, ``'PLAYER_NAME'``, ``'GAME_ID'``, ``'DFGA'``, ``'PLAYER_ID'``

  ``'team-stats'``
    ``'DFGM'``, ``'DFG_PCT'``, ``'RBC'``, ``'CFGA'``, ``'TCHS'``, ``'TEAM_ABBREVIATION'``, ``'PASS'``, ``'TEAM_CITY'``, ``'DIST'``, ``'FTAST'``, ``'UFG_PCT'``, ``'FG_PCT'``, ``'AST'``, ``'TEAM_NICKNAME'``, ``'DFGA'``, ``'ORBC'``, ``'SAST'``, ``'CFG_PCT'``, ``'GAME_ID'``, ``'UFGM'``

    

.. _request-game-boxscore-usage:

game-boxscore-usage
-------------------------------


Required Parameters:
  :ref:`GameID <param-gameid>`

Optional Parameters:
  :ref:`EndPeriod <param-endperiod>`, :ref:`EndRange <param-endrange>`, :ref:`RangeType <param-rangetype>`, :ref:`StartPeriod <param-startperiod>`, :ref:`StartRange <param-startrange>`

Return Fields:
  ``'player-stats'``
    ``'PCT_REB'``, ``'USG_PCT'``, ``'PCT_FGA'``, ``'TEAM_ABBREVIATION'``, ``'PCT_FTM'``, ``'PCT_TOV'``, ``'PCT_AST'``, ``'PCT_FGM'``, ``'PCT_STL'``, ``'START_POSITION'``, ``'PLAYER_ID'``, ``'TEAM_CITY'``, ``'PCT_FG3A'``, ``'PCT_OREB'``, ``'PCT_DREB'``, ``'PCT_FTA'``, ``'PCT_FG3M'``, ``'PLAYER_NAME'``, ``'GAME_ID'``, ``'COMMENT'``, ``'PCT_PF'``, ``'MIN'``, ``'PCT_PFD'``, ``'PCT_BLKA'``, ``'PCT_BLK'``

  ``'team-stats'``
    ``'PCT_REB'``, ``'USG_PCT'``, ``'PCT_FGA'``, ``'TEAM_ABBREVIATION'``, ``'PCT_FTM'``, ``'PCT_TOV'``, ``'PCT_AST'``, ``'PCT_FGM'``, ``'PCT_STL'``, ``'MIN'``, ``'PCT_FG3A'``, ``'PCT_OREB'``, ``'PCT_DREB'``, ``'PCT_FTA'``, ``'PCT_FG3M'``, ``'TEAM_NAME'``, ``'GAME_ID'``, ``'PCT_PTS'``, ``'PCT_PF'``, ``'TEAM_CITY'``, ``'PCT_PFD'``, ``'PCT_BLKA'``

    

.. _request-game-play-by-play:

game-play-by-play
-------------------------------


Required Parameters:
  :ref:`GameID <param-gameid>`

Optional Parameters:
  :ref:`EndPeriod <param-endperiod>`, :ref:`StartPeriod <param-startperiod>`

Return Fields:
  ``'plays'``
    ``'EVENTMSGTYPE'``, ``'PERSON3TYPE'``, ``'SCOREMARGIN'``, ``'WCTIMESTRING'``, ``'EVENTMSGACTIONTYPE'``, ``'PLAYER2_TEAM_ID'``, ``'HOMEDESCRIPTION'``, ``'PLAYER2_NAME'``, ``'PLAYER3_NAME'``, ``'PLAYER1_NAME'``, ``'NEUTRALDESCRIPTION'``, ``'PLAYER1_TEAM_NICKNAME'``, ``'PERSON1TYPE'``, ``'PLAYER2_TEAM_CITY'``, ``'PLAYER1_ID'``, ``'PLAYER1_TEAM_ID'``, ``'PLAYER3_TEAM_ABBREVIATION'``, ``'PLAYER2_TEAM_ABBREVIATION'``, ``'PLAYER2_ID'``, ``'EVENTNUM'``, ``'PCTIMESTRING'``, ``'GAME_ID'``, ``'PERIOD'``, ``'SCORE'``, ``'VISITORDESCRIPTION'``, ``'PLAYER1_TEAM_ABBREVIATION'``, ``'PLAYER1_TEAM_CITY'``, ``'PLAYER3_ID'``, ``'PLAYER3_TEAM_NICKNAME'``, ``'PLAYER3_TEAM_CITY'``, ``'PLAYER3_TEAM_ID'``, ``'PLAYER2_TEAM_NICKNAME'``

  ``'available-video'``
    

    

.. _request-league-classic-stats:

league-classic-stats
-------------------------------


Required Parameters:
  :ref:`Season <param-season>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameScope <param-gamescope>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`MeasureType <param-measuretype>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`PaceAdjust <param-paceadjust>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`PlayerExperience <param-playerexperience>`, :ref:`PlayerPosition <param-playerposition>`, :ref:`PlusMinus <param-plusminus>`, :ref:`Rank <param-rank>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`StarterBench <param-starterbench>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'stats'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'FTM'``, ``'L'``, ``'W'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'CFPARAMS'``, ``'DREB'``, ``'FG3M'``, ``'CFID'``, ``'AST'``, ``'PF'``, ``'BLKA'``, ``'FG3_PCT'``, ``'PFD'``, ``'TEAM_NAME'``, ``'FG3A'``, ``'TOV'``, ``'TEAM_ID'``, ``'PLUS_MINUS'``, ``'OREB'``, ``'MIN'``

    

.. _request-league-clutch-stats:

league-clutch-stats
-------------------------------
.. warning:: This request cannot be executed due to issues with the current implementation of NBAWebStats. These issues will likely be addressed by upcoming versions of NBAWebStats at which point the request will become available.

Required Parameters:
  :ref:`Season <param-season>`

Optional Parameters:
  :ref:`AheadBehind <param-aheadbehind>`, :ref:`ClutchTime <param-clutchtime>`, :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameScope <param-gamescope>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`MeasureType <param-measuretype>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`PaceAdjust <param-paceadjust>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`PlayerExperience <param-playerexperience>`, :ref:`PlayerPosition <param-playerposition>`, :ref:`PlusMinus <param-plusminus>`, :ref:`PointDiff <param-pointdiff>`, :ref:`Rank <param-rank>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`StarterBench <param-starterbench>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'clutch'``
    

    

.. _request-league-daily-scoreboard:

league-daily-scoreboard
-------------------------------
.. warning:: This request has been restricted by nba.com.


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'game-header'``
    

  ``'linescore'``
    

  ``'series-standings'``
    

  ``'last-meeting'``
    

  ``'eastern-conference-standings'``
    

  ``'western-conference-standings'``
    

  ``'available'``
    

  ``'team-leaders'``
    

  ``'ticket-links'``
    

  ``'win-probability'``
    

    

.. _request-league-franchise-history:

league-franchise-history
-------------------------------


Required Parameters:
  

Optional Parameters:
  :ref:`LeagueID <param-leagueid>`

Return Fields:
  ``'current-teams'``
    ``'YEARS'``, ``'LOSSES'``, ``'WINS'``, ``'GAMES'``, ``'WIN_PCT'``, ``'CONF_TITLES'``, ``'TEAM_NAME'``, ``'PO_APPEARANCES'``, ``'DIV_TITLES'``, ``'START_YEAR'``, ``'TEAM_CITY'``

  ``'defunct-teams'``
    ``'YEARS'``, ``'LOSSES'``, ``'WINS'``, ``'GAMES'``, ``'WIN_PCT'``, ``'CONF_TITLES'``, ``'TEAM_NAME'``, ``'PO_APPEARANCES'``, ``'DIV_TITLES'``, ``'START_YEAR'``, ``'TEAM_CITY'``

    

.. _request-league-leaders:

league-leaders
-------------------------------
.. warning:: This request cannot be executed due to issues with the current implementation of NBAWebStats. These issues will likely be addressed by upcoming versions of NBAWebStats at which point the request will become available.

Required Parameters:
  :ref:`Season <param-season>`

Optional Parameters:
  :ref:`LeagueID <param-leagueid>`, :ref:`PerMode <param-permode>`, :ref:`Scope <param-scope>`, :ref:`SeasonType <param-seasontype>`, :ref:`StatCategory <param-statcategory>`

Return Fields:
  ``'leaders'``
    

    

.. _request-league-lineups:

league-lineups
-------------------------------


Required Parameters:
  :ref:`Season <param-season>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`Direction <param-direction>`, :ref:`GameSegment <param-gamesegment>`, :ref:`GroupQuantity <param-groupquantity>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`MeasureType <param-measuretype>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`PaceAdjust <param-paceadjust>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`PlayerOrTeam <param-playerorteam>`, :ref:`PlusMinus <param-plusminus>`, :ref:`Rank <param-rank>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`Sorter <param-sorter>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'lineups'``
    ``'GROUP_NAME'``, ``'BLK'``, ``'PTS'``, ``'GP'``, ``'GROUP_ID'``, ``'TEAM_ABBREVIATION'``, ``'L'``, ``'W'``, ``'OREB'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'DREB'``, ``'FG3M'``, ``'AST'``, ``'PF'``, ``'BLKA'``, ``'FG3_PCT'``, ``'PFD'``, ``'FTM'``, ``'FG3A'``, ``'TOV'``, ``'TEAM_ID'``, ``'PLUS_MINUS'``, ``'GROUP_SET'``, ``'MIN'``, ``'FG_PCT'``, ``'REB'``

    

.. _request-league-playoff-picture:

league-playoff-picture
-------------------------------


Required Parameters:
  :ref:`SeasonID <param-seasonid>`

Optional Parameters:
  :ref:`LeagueID <param-leagueid>`

Return Fields:
  ``'eastern-conf-playoff-picture'``
    ``'HIGH_SEED_SERIES_REMAINING_HOME_G'``, ``'HIGH_SEED_SERIES_REMAINING_G'``, ``'LOW_SEED_TEAM_ID'``, ``'HIGH_SEED_SERIES_W'``, ``'HIGH_SEED_TEAM_ID'``, ``'LOW_SEED_TEAM'``, ``'HIGH_SEED_RANK'``, ``'HIGH_SEED_SERIES_L'``, ``'HIGH_SEED_TEAM'``, ``'LOW_SEED_RANK'``, ``'CONFERENCE'``

  ``'western-conf-playoff-picture'``
    ``'HIGH_SEED_SERIES_REMAINING_HOME_G'``, ``'HIGH_SEED_SERIES_REMAINING_G'``, ``'LOW_SEED_TEAM_ID'``, ``'HIGH_SEED_SERIES_W'``, ``'HIGH_SEED_TEAM_ID'``, ``'LOW_SEED_TEAM'``, ``'HIGH_SEED_RANK'``, ``'HIGH_SEED_SERIES_L'``, ``'HIGH_SEED_TEAM'``, ``'LOW_SEED_RANK'``, ``'CONFERENCE'``

  ``'eastern-conf-standing'``
    ``'LOSSES'``, ``'WINS'``, ``'SOSA_REMAINING'``, ``'GR_UNDER_500'``, ``'AWAY'``, ``'RANKING_CRITERIA'``, ``'CLINCHED_CONFERENCE'``, ``'GB'``, ``'TEAM'``, ``'HOME'``, ``'CONFERENCE'``, ``'ELIMINATED_PLAYOFFS'``, ``'GR_OVER_500_AWAY'``, ``'CONF'``, ``'RANK'``, ``'CLINCHED_PLAYOFFS'``, ``'CLINCHED_DIVISION'``, ``'GR_OVER_500'``, ``'TEAM_ID'``, ``'GR_UNDER_500_AWAY'``

  ``'western-conf-standing'``
    ``'LOSSES'``, ``'WINS'``, ``'SOSA_REMAINING'``, ``'GR_UNDER_500'``, ``'AWAY'``, ``'RANKING_CRITERIA'``, ``'CLINCHED_CONFERENCE'``, ``'GB'``, ``'TEAM'``, ``'HOME'``, ``'CONFERENCE'``, ``'ELIMINATED_PLAYOFFS'``, ``'GR_OVER_500_AWAY'``, ``'CONF'``, ``'RANK'``, ``'CLINCHED_PLAYOFFS'``, ``'CLINCHED_DIVISION'``, ``'GR_OVER_500'``, ``'TEAM_ID'``, ``'GR_UNDER_500_AWAY'``

  ``'eastern-conf-remaining-games'``
    ``'TEAM'``, ``'REMAINING_G'``, ``'TEAM_ID'``, ``'REMAINING_HOME_G'``

  ``'western-conf-remaining-games'``
    ``'TEAM'``, ``'REMAINING_G'``, ``'TEAM_ID'``, ``'REMAINING_HOME_G'``

    

.. _request-league-team-shot-locations:

league-team-shot-locations
-------------------------------
.. warning:: This request cannot be executed due to issues with the current implementation of NBAWebStats. These issues will likely be addressed by upcoming versions of NBAWebStats at which point the request will become available.

Required Parameters:
  :ref:`Season <param-season>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`DistanceRange <param-distancerange>`, :ref:`GameScope <param-gamescope>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`MeasureType <param-measuretype>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`PaceAdjust <param-paceadjust>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`PlayerExperience <param-playerexperience>`, :ref:`PlayerPosition <param-playerposition>`, :ref:`PlusMinus <param-plusminus>`, :ref:`Rank <param-rank>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`StarterBench <param-starterbench>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'shooting'``
    

    

.. _request-league-transactions:

league-transactions
-------------------------------


Required Parameters:
  

Optional Parameters:
  

    

.. _request-player-career-stats:

player-career-stats
-------------------------------


Required Parameters:
  :ref:`PlayerID <param-playerid>`

Optional Parameters:
  :ref:`LeagueID <param-leagueid>`, :ref:`PerMode <param-permode>`

Return Fields:
  ``'season-totals-regular'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'GS'``, ``'TEAM_ABBREVIATION'``, ``'FG_PCT'``, ``'SEASON_ID'``, ``'TEAM_ID'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'DREB'``, ``'FG3M'``, ``'AST'``, ``'PF'``, ``'FG3_PCT'``, ``'FTM'``, ``'FG3A'``, ``'TOV'``, ``'PLAYER_ID'``, ``'PLAYER_AGE'``, ``'FGM'``, ``'MIN'``, ``'REB'``, ``'OREB'``

  ``'career-totals-regular'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'GS'``, ``'FG_PCT'``, ``'TEAM_ID'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'DREB'``, ``'FG3M'``, ``'AST'``, ``'PF'``, ``'FG3_PCT'``, ``'FTM'``, ``'FG3A'``, ``'TOV'``, ``'PLAYER_ID'``, ``'FGM'``

  ``'season-totals-post'``
    

  ``'career-totals-post'``
    

  ``'season-totals-allstar'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'GS'``, ``'TEAM_ABBREVIATION'``, ``'FG_PCT'``, ``'SEASON_ID'``, ``'TEAM_ID'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'DREB'``, ``'FG3M'``, ``'AST'``, ``'PF'``, ``'FG3_PCT'``, ``'FTM'``, ``'FG3A'``, ``'TOV'``, ``'PLAYER_ID'``, ``'PLAYER_AGE'``, ``'FGM'``, ``'MIN'``, ``'REB'``, ``'OREB'``

  ``'career-totals-allstar'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'GS'``, ``'FG_PCT'``, ``'TEAM_ID'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'DREB'``, ``'FG3M'``, ``'AST'``, ``'PF'``, ``'FG3_PCT'``, ``'FTM'``, ``'FG3A'``, ``'TOV'``, ``'PLAYER_ID'``, ``'FGM'``

  ``'season-totals-college'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'GS'``, ``'FG_PCT'``, ``'SEASON_ID'``, ``'PLAYER_AGE'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'DREB'``, ``'FG3M'``, ``'AST'``, ``'PF'``, ``'FG3_PCT'``, ``'FTM'``, ``'SCHOOL_NAME'``, ``'FG3A'``, ``'TOV'``, ``'PLAYER_ID'``, ``'ORGANIZATION_ID'``, ``'OREB'``

  ``'career-totals-college'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'GS'``, ``'FG_PCT'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'DREB'``, ``'FG3M'``, ``'AST'``, ``'PF'``, ``'FG3_PCT'``, ``'FTM'``, ``'FG3A'``, ``'TOV'``, ``'PLAYER_ID'``, ``'ORGANIZATION_ID'``, ``'FGM'``, ``'MIN'``, ``'REB'``, ``'OREB'``

  ``'season-rankings-regular'``
    ``'RANK_PTS'``, ``'RANK_FG3_PCT'``, ``'RANK_TOV'``, ``'GP'``, ``'GS'``, ``'TEAM_ABBREVIATION'``, ``'RANK_BLK'``, ``'SEASON_ID'``, ``'RANK_OREB'``, ``'TEAM_ID'``, ``'RANK_FGM'``, ``'RANK_AST'``, ``'RANK_FT_PCT'``, ``'RANK_FG_PCT'``, ``'RANK_STL'``, ``'RANK_EFF'``, ``'RANK_FG3A'``, ``'RANK_DREB'``, ``'PLAYER_ID'``, ``'RANK_FG3M'``, ``'RANK_MIN'``, ``'RANK_FTA'``, ``'PLAYER_AGE'``, ``'RANK_FTM'``

  ``'season-rankings-post'``
    

  ``'season-high'``
    ``'GAME_DATE'``, ``'STAT_VALUE'``, ``'GAME_ID'``, ``'PLAYER_ID'``, ``'VS_TEAM_ABBREVIATION'``, ``'STAT'``, ``'VS_TEAM_ID'``, ``'DATE_EST'``, ``'STAT_ORDER'``, ``'VS_TEAM_NAME'``

  ``'career-high'``
    ``'GAME_DATE'``, ``'STAT_VALUE'``, ``'GAME_ID'``, ``'PLAYER_ID'``, ``'VS_TEAM_ABBREVIATION'``, ``'STAT'``, ``'VS_TEAM_ID'``, ``'DATE_EST'``, ``'STAT_ORDER'``, ``'VS_TEAM_NAME'``

  ``'next-game'``
    ``'GAME_ID'``, ``'GAME_DATE'``, ``'PLAYER_TEAM_NICKNAME'``, ``'PLAYER_TEAM_CITY'``, ``'PLAYER_TEAM_ABBREVIATION'``, ``'PLAYER_TEAM_ID'``, ``'VS_TEAM_ABBREVIATION'``, ``'VS_TEAM_ID'``, ``'VS_TEAM_NICKNAME'``, ``'VS_TEAM_CITY'``

    

.. _request-player-defense-dashboard:

player-defense-dashboard
-------------------------------


Required Parameters:
  :ref:`PlayerID <param-playerid>`, :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'defending-shot'``
    

    

.. _request-player-demographics:

player-demographics
-------------------------------


Required Parameters:
  :ref:`PlayerID <param-playerid>`

Optional Parameters:
  

Return Fields:
  ``'player-info'``
    ``'PLAYERCODE'``, ``'SEASON_EXP'``, ``'DISPLAY_FI_LAST'``, ``'WEIGHT'``, ``'TEAM_ABBREVIATION'``, ``'TO_YEAR'``, ``'PERSON_ID'``, ``'TEAM_CITY'``, ``'LAST_AFFILIATION'``, ``'BIRTHDATE'``, ``'COUNTRY'``, ``'TEAM_CODE'``, ``'FROM_YEAR'``, ``'GAMES_PLAYED_FLAG'``, ``'DISPLAY_FIRST_LAST'``, ``'SCHOOL'``, ``'LAST_NAME'``, ``'FIRST_NAME'``, ``'TEAM_NAME'``, ``'ROSTERSTATUS'``, ``'TEAM_ID'``, ``'DLEAGUE_FLAG'``, ``'POSITION'``

  ``'headline-stats'``
    ``'PIE'``, ``'TimeFrame'``, ``'PTS'``, ``'PLAYER_ID'``, ``'AST'``, ``'REB'``

    

.. _request-player-game-logs:

player-game-logs
-------------------------------


Required Parameters:
  :ref:`PlayerID <param-playerid>`, :ref:`Season <param-season>`

Optional Parameters:
  :ref:`SeasonType <param-seasontype>`

Return Fields:
  ``'logs'``
    ``'BLK'``, ``'PTS'``, ``'VIDEO_AVAILABLE'``, ``'WL'``, ``'FG_PCT'``, ``'SEASON_ID'``, ``'Game_ID'``, ``'FGA'``, ``'FT_PCT'``, ``'Player_ID'``, ``'FTA'``, ``'DREB'``, ``'FG3M'``, ``'AST'``, ``'PF'``, ``'FG3_PCT'``, ``'FGM'``, ``'FTM'``, ``'FG3A'``, ``'GAME_DATE'``, ``'TOV'``, ``'PLUS_MINUS'``

    

.. _request-player-general-splits:

player-general-splits
-------------------------------
.. warning:: This request has been restricted by nba.com.


Required Parameters:
  :ref:`PlayerID <param-playerid>`, :ref:`Season <param-season>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`MeasureType <param-measuretype>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`PaceAdjust <param-paceadjust>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`PlusMinus <param-plusminus>`, :ref:`Rank <param-rank>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'overall'``
    

  ``'location'``
    

  ``'wins-losses'``
    

  ``'month'``
    

  ``'pre-post-allstar'``
    

  ``'starting-position'``
    

  ``'days-rest'``
    

    

.. _request-player-passing-dashboard:

player-passing-dashboard
-------------------------------


Required Parameters:
  :ref:`PlayerID <param-playerid>`, :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'passes-made'``
    

  ``'passes-received'``
    

    

.. _request-player-rebound-dashboard:

player-rebound-dashboard
-------------------------------


Required Parameters:
  :ref:`PlayerID <param-playerid>`, :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'overall'``
    

  ``'shot-type'``
    

  ``'contesting-rebounders'``
    

  ``'shot-distance'``
    

  ``'rebound-distance'``
    

    

.. _request-player-rebound-log:

player-rebound-log
-------------------------------
.. warning:: This request has been deprecated by nba.com.


Required Parameters:
  :ref:`PlayerID <param-playerid>`, :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`Period <param-period>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'log'``
    

    

.. _request-player-shot-chart:

player-shot-chart
-------------------------------


Required Parameters:
  :ref:`GameID <param-gameid>`, :ref:`PlayerID <param-playerid>`, :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`AheadBehind <param-aheadbehind>`, :ref:`ClutchTime <param-clutchtime>`, :ref:`ContextFilter <param-contextfilter>`, :ref:`ContextMeasure <param-contextmeasure>`, :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`EndPeriod <param-endperiod>`, :ref:`EndRange <param-endrange>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`Period <param-period>`, :ref:`Position <param-position>`, :ref:`RangeType <param-rangetype>`, :ref:`RookieYear <param-rookieyear>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`StartPeriod <param-startperiod>`, :ref:`StartRange <param-startrange>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'chart'``
    

  ``'leagueaverage'``
    ``'GRID_TYPE'``, ``'FG_PCT'``, ``'SHOT_ZONE_BASIC'``

    

.. _request-player-shot-dashboard:

player-shot-dashboard
-------------------------------


Required Parameters:
  :ref:`PlayerID <param-playerid>`, :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'overall'``
    

  ``'general'``
    

  ``'shot-clock'``
    

  ``'dribble'``
    

  ``'closest-defender'``
    

  ``'closest-defender-10ft'``
    

  ``'touch-time'``
    

    

.. _request-player-shot-log:

player-shot-log
-------------------------------
.. warning:: This request has been deprecated by nba.com.


Required Parameters:
  :ref:`PlayerID <param-playerid>`, :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`Period <param-period>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'log'``
    

    

.. _request-playtype-player-cut:

playtype-player-cut
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

  ``'defensive'``
    

    

.. _request-playtype-player-handoff:

playtype-player-handoff
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

  ``'defensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

    

.. _request-playtype-player-isolation:

playtype-player-isolation
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

  ``'defensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

    

.. _request-playtype-player-misc:

playtype-player-misc
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

  ``'defensive'``
    

    

.. _request-playtype-player-offrebound:

playtype-player-offrebound
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

  ``'defensive'``
    

    

.. _request-playtype-player-offscreen:

playtype-player-offscreen
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

  ``'defensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

    

.. _request-playtype-player-postup:

playtype-player-postup
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

  ``'defensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

    

.. _request-playtype-player-pr-ball-handler:

playtype-player-pr-ball-handler
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

  ``'defensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

    

.. _request-playtype-player-pr-roll-man:

playtype-player-pr-roll-man
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

  ``'defensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

    

.. _request-playtype-player-spotup:

playtype-player-spotup
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

  ``'defensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

    

.. _request-playtype-player-transition:

playtype-player-transition
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'PlayerFirstName'``, ``'PlayerNumber'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PlayerIDSID'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'PlayerLastName'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'P'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``, ``'WorsePPP'``, ``'FT'``

  ``'defensive'``
    

    

.. _request-playtype-team-cut:

playtype-team-cut
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

  ``'defensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

    

.. _request-playtype-team-handoff:

playtype-team-handoff
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

  ``'defensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

    

.. _request-playtype-team-isolation:

playtype-team-isolation
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

  ``'defensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

    

.. _request-playtype-team-misc:

playtype-team-misc
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

  ``'defensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

    

.. _request-playtype-team-offrebound:

playtype-team-offrebound
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

  ``'defensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

    

.. _request-playtype-team-offscreen:

playtype-team-offscreen
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

  ``'defensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

    

.. _request-playtype-team-postup:

playtype-team-postup
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

  ``'defensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

    

.. _request-playtype-team-pr-ball-handler:

playtype-team-pr-ball-handler
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

  ``'defensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

    

.. _request-playtype-team-pr-roll-man:

playtype-team-pr-roll-man
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

  ``'defensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

    

.. _request-playtype-team-spotup:

playtype-team-spotup
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

  ``'defensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

    

.. _request-playtype-team-transition:

playtype-team-transition
-------------------------------


Required Parameters:
  

Optional Parameters:
  

Return Fields:
  ``'offensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

  ``'defensive'``
    ``'TeamName'``, ``'GP'``, ``'FGmG'``, ``'FGAG'``, ``'TeamIDSID'``, ``'PPG'``, ``'TeamNameAbbreviation'``, ``'Points'``, ``'TeamShortName'``, ``'FGA'``, ``'FG'``, ``'SF'``, ``'PossG'``, ``'PlusOne'``, ``'Time'``, ``'TO'``, ``'PPP'``, ``'FGMG'``, ``'FGm'``, ``'aFG'``, ``'Poss'``, ``'BetterPPP'``

    

.. _request-sportvu-catch-and-shoot:

sportvu-catch-and-shoot
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'FG3M'``, ``'PTS'``, ``'GP'``, ``'LAST_NAME'``, ``'FIRST_NAME'``, ``'TEAM_ABBREVIATION'``, ``'FG_PCT'``, ``'FG3A'``, ``'PLAYER_ID'``, ``'PTS_TOT'``, ``'PLAYER'``, ``'FGA'``, ``'MIN'``, ``'EFG_PCT'``

    

.. _request-sportvu-defense:

sportvu-defense
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'BLK'``, ``'GP'``, ``'LAST_NAME'``, ``'FIRST_NAME'``, ``'TEAM_ABBREVIATION'``, ``'BLK_TOT'``, ``'PLAYER_ID'``, ``'STL'``, ``'FGP_DEFEND_RIM'``, ``'PLAYER'``, ``'MIN'``, ``'FGA_DEFEND_RIM'``

    

.. _request-sportvu-drives:

sportvu-drives
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'GP'``, ``'DVS_TOT'``, ``'PTS_48'``, ``'LAST_NAME'``, ``'DTP'``, ``'FIRST_NAME'``, ``'TEAM_ABBREVIATION'``, ``'FG_PCT'``, ``'DVS'``

    

.. _request-sportvu-passing:

sportvu-passing
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'AST_TOT'``, ``'AST'``, ``'GP'``, ``'LAST_NAME'``, ``'FIRST_NAME'``, ``'TEAM_ABBREVIATION'``, ``'PTS_CRT'``, ``'PASS'``, ``'PLAYER_ID'``, ``'PLAYER'``, ``'PTS_CRT_48'``, ``'MIN'``, ``'AST_SEC'``, ``'AST_POT'``

    

.. _request-sportvu-pull-up-shooting:

sportvu-pull-up-shooting
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'FG3M'``, ``'PTS'``, ``'GP'``, ``'LAST_NAME'``, ``'FIRST_NAME'``, ``'TEAM_ABBREVIATION'``, ``'FG_PCT'``, ``'FG3A'``, ``'PLAYER_ID'``, ``'PTS_TOT'``, ``'PLAYER'``, ``'FGA'``, ``'MIN'``, ``'EFG_PCT'``

    

.. _request-sportvu-rebounding:

sportvu-rebounding
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'REB_UNCONTESTED'``, ``'GP'``, ``'TEAM_ABBREVIATION'``, ``'DREB_CONTESTED'``, ``'OREB_COL_PCT'``, ``'DREB'``, ``'OREB_UNCONTESTED_PCT'``, ``'PLAYER'``, ``'REB_COL_PCT'``, ``'REB'``, ``'OREB_CONTESTED'``, ``'REB_TOT'``, ``'OREB_CHANCE'``, ``'LAST_NAME'``, ``'REB_CHANCE'``, ``'REB_UNCONTESTED_PCT'``, ``'DREB_UNCONTESTED'``, ``'MIN'``, ``'DREB_COL_PCT'``, ``'PLAYER_ID'``, ``'OREB_UNCONTESTED'``, ``'DREB_CHANCE'``, ``'DREB_UNCONTESTED_PCT'``, ``'REB_CONTESTED'``, ``'FIRST_NAME'``

    

.. _request-sportvu-shooting:

sportvu-shooting
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'CFG3P'``, ``'PTS'``, ``'CFG3A'``, ``'GP'``, ``'TEAM_ABBREVIATION'``, ``'UFG3P'``, ``'FGA_CATCH_SHOOT'``, ``'FGP_CLOSE'``, ``'EFG_PCT'``, ``'FGA_PULL_UP'``, ``'PLAYER'``, ``'PTS_CATCH_SHOOT'``, ``'UFGP'``, ``'UFG3M'``, ``'PTS_PULL_UP'``, ``'FGP_DRIVE'``, ``'CFG3M'``, ``'CFGA'``, ``'CFGP'``, ``'LAST_NAME'``, ``'FIRST_NAME'``, ``'FGP_PULL_UP'``, ``'PTS_CLOSE'``, ``'UFGM'``, ``'UFG3A'``, ``'PLAYER_ID'``, ``'CFGM'``, ``'UFGA'``, ``'FGA_CLOSE'``, ``'PTS_DRIVE'``, ``'MIN'``

    

.. _request-sportvu-speed:

sportvu-speed
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'GP'``, ``'DIST_48'``, ``'DIST_PG'``, ``'AV_SPD_OFF'``, ``'LAST_NAME'``, ``'FIRST_NAME'``, ``'TEAM_ABBREVIATION'``, ``'AV_SPD_DEF'``, ``'AV_SPD'``, ``'PLAYER_ID'``, ``'PLAYER'``, ``'DIST'``, ``'MIN'``

    

.. _request-sportvu-team-catch-and-shoot:

sportvu-team-catch-and-shoot
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'FG3M'``, ``'PTS'``, ``'GP'``, ``'FG3_PCT'``, ``'TEAM_ABBREVIATION'``, ``'TEAM_NAME'``, ``'FG_PCT'``, ``'FG3A'``, ``'EFG_PCT'``, ``'TEAM_CITY'``, ``'PTS_TOT'``, ``'MIN'``, ``'FGA'``, ``'TEAM_CODE'``, ``'FGM'``

    

.. _request-sportvu-team-defense:

sportvu-team-defense
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'BLK'``, ``'GP'``, ``'TEAM_ABBREVIATION'``, ``'TEAM_NAME'``, ``'BLK_TOT'``, ``'TEAM_ID'``, ``'TEAM_CITY'``, ``'STL'``, ``'FGP_DEFEND_RIM'``, ``'MIN'``, ``'TEAM_CODE'``

    

.. _request-sportvu-team-drives:

sportvu-team-drives
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'GP'``, ``'DVS_TOT'``, ``'PTS_48'``, ``'DTP'``, ``'TEAM_ABBREVIATION'``, ``'TEAM_NAME'``, ``'FG_PCT'``, ``'DVS'``, ``'DPP_TOT'``, ``'TEAM_ID'``

    

.. _request-sportvu-team-passing:

sportvu-team-passing
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'AST_TOT'``, ``'AST'``, ``'GP'``, ``'PTS_CRT'``, ``'TEAM_ABBREVIATION'``, ``'TEAM_NAME'``, ``'PASS'``, ``'TEAM_ID'``, ``'TEAM_CITY'``, ``'TEAM_CODE'``, ``'PTS_CRT_48'``, ``'MIN'``

    

.. _request-sportvu-team-pull-up-shooting:

sportvu-team-pull-up-shooting
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'FG3M'``, ``'PTS'``, ``'GP'``, ``'FG3_PCT'``, ``'TEAM_ABBREVIATION'``, ``'TEAM_NAME'``, ``'FG_PCT'``, ``'FG3A'``, ``'EFG_PCT'``, ``'TEAM_CITY'``, ``'PTS_TOT'``, ``'MIN'``, ``'FGA'``, ``'TEAM_CODE'``, ``'FGM'``

    

.. _request-sportvu-team-rebounding:

sportvu-team-rebounding
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'REB_UNCONTESTED'``, ``'GP'``, ``'REB_UNCONTESTED_PCT'``, ``'TEAM_ABBREVIATION'``, ``'DREB_CONTESTED'``, ``'OREB_COL_PCT'``, ``'OREB_UNCONTESTED_PCT'``, ``'TEAM_CITY'``, ``'DREB_UNCONTESTED_PCT'``, ``'TEAM_CODE'``, ``'REB_COL_PCT'``, ``'OREB_CONTESTED'``, ``'REB_TOT'``, ``'REB_CONTESTED'``, ``'REB_CHANCE'``, ``'TEAM_NAME'``, ``'DREB_UNCONTESTED'``, ``'DREB_COL_PCT'``, ``'OREB_CHANCE'``, ``'TEAM_ID'``, ``'OREB_UNCONTESTED'``, ``'DREB'``, ``'DREB_CHANCE'``, ``'MIN'``

    

.. _request-sportvu-team-shooting:

sportvu-team-shooting
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'PTS_CLOSE'``, ``'CFG3P'``, ``'PTS'``, ``'CFG3A'``, ``'GP'``, ``'TEAM_ABBREVIATION'``, ``'UFG3P'``, ``'FGP_CLOSE'``, ``'EFG_PCT'``, ``'TEAM_CITY'``, ``'FGA_PULL_UP'``, ``'PTS_CATCH_SHOOT'``, ``'TEAM_CODE'``, ``'UFGP'``, ``'UFG3M'``, ``'PTS_PULL_UP'``, ``'FGP_DRIVE'``, ``'CFG3M'``, ``'CFGA'``, ``'CFGP'``, ``'FGP_PULL_UP'``, ``'TEAM_NAME'``, ``'FGA_CATCH_SHOOT'``, ``'UFGM'``, ``'UFG3A'``, ``'TEAM_ID'``, ``'CFGM'``, ``'UFGA'``, ``'FGA_CLOSE'``, ``'PTS_DRIVE'``

    

.. _request-sportvu-team-speed:

sportvu-team-speed
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'GP'``, ``'DIST_48'``, ``'DIST_PG'``, ``'AV_SPD_OFF'``, ``'TEAM_CODE'``, ``'TEAM_ABBREVIATION'``, ``'TEAM_NAME'``, ``'AV_SPD_DEF'``, ``'AV_SPD'``, ``'TEAM_ID'``, ``'TEAM_CITY'``, ``'DIST'``, ``'MIN'``

    

.. _request-sportvu-team-touches:

sportvu-team-touches
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'TCH_TOT'``, ``'PTS_HCCT'``, ``'PTS'``, ``'TCH'``, ``'GP'``, ``'FC_TCH'``, ``'TEAM_ABBREVIATION'``, ``'TEAM_NAME'``, ``'TEAM_CODE'``, ``'CL_TCH'``, ``'TEAM_CITY'``, ``'PTS_TCH'``, ``'EL_TCH'``, ``'MIN'``

    

.. _request-sportvu-touches:

sportvu-touches
-------------------------------


Required Parameters:
  :ref:`Year <param-year>`

Optional Parameters:
  

Return Fields:
  ``'data'``
    ``'TCH_TOT'``, ``'PTS_HCCT'``, ``'PTS'``, ``'TCH'``, ``'GP'``, ``'LAST_NAME'``, ``'FIRST_NAME'``, ``'TEAM_ABBREVIATION'``, ``'PLAYER_ID'``, ``'FC_TCH'``, ``'CL_TCH'``, ``'EL_TCH'``, ``'PTS_TCH'``

    

.. _request-team-game-logs:

team-game-logs
-------------------------------


Required Parameters:
  :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`SeasonType <param-seasontype>`

Return Fields:
  ``'logs'``
    ``'BLK'``, ``'PTS'``, ``'WL'``, ``'FG_PCT'``, ``'FGM'``, ``'Game_ID'``, ``'FGA'``, ``'FT_PCT'``, ``'Team_ID'``, ``'FTA'``, ``'DREB'``, ``'FG3M'``, ``'AST'``, ``'PF'``, ``'FG3_PCT'``, ``'FTM'``, ``'FG3A'``, ``'GAME_DATE'``, ``'TOV'``

    

.. _request-team-history:

team-history
-------------------------------


Required Parameters:
  :ref:`TeamID <param-teamid>`

Optional Parameters:
  

    

.. _request-team-info:

team-info
-------------------------------


Required Parameters:
  :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`LeagueID <param-leagueid>`, :ref:`SeasonType <param-seasontype>`

Return Fields:
  ``'info'``
    ``'MAX_YEAR'``, ``'SEASON_YEAR'``, ``'TEAM_CODE'``, ``'TEAM_NAME'``, ``'TEAM_ABBREVIATION'``, ``'L'``, ``'MIN_YEAR'``, ``'TEAM_CONFERENCE'``, ``'DIV_RANK'``, ``'TEAM_ID'``, ``'TEAM_CITY'``

  ``'season-ranks'``
    ``'OPP_PTS_RANK'``, ``'TEAM_ID'``, ``'REB_RANK'``, ``'AST_RANK'``, ``'PTS_PG'``, ``'AST_PG'``, ``'SEASON_ID'``, ``'REB_PG'``

    

.. _request-team-lineups:

team-lineups
-------------------------------


Required Parameters:
  :ref:`GameID <param-gameid>`, :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameSegment <param-gamesegment>`, :ref:`GroupQuantity <param-groupquantity>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`MeasureType <param-measuretype>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`PaceAdjust <param-paceadjust>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`PlusMinus <param-plusminus>`, :ref:`Rank <param-rank>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'overall'``
    

  ``'lineups'``
    

    

.. _request-team-on-off-court:

team-on-off-court
-------------------------------


Required Parameters:
  :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`MeasureType <param-measuretype>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`PaceAdjust <param-paceadjust>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`PlusMinus <param-plusminus>`, :ref:`Rank <param-rank>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'overall'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'FTM'``, ``'TEAM_ABBREVIATION'``, ``'L'``, ``'W'``, ``'FGM'``, ``'GROUP_VALUE'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'DREB'``, ``'FG3M'``, ``'AST'``, ``'PF'``, ``'W_PCT'``, ``'FG3_PCT'``, ``'PFD'``, ``'TEAM_NAME'``, ``'FG3A'``, ``'TOV'``, ``'TEAM_ID'``, ``'PLUS_MINUS'``, ``'OREB'``, ``'MIN'``, ``'FG_PCT'``

  ``'on-court'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'FTM'``, ``'TEAM_ABBREVIATION'``, ``'L'``, ``'W'``, ``'FGM'``, ``'OREB'``, ``'STL'``, ``'COURT_STATUS'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'DREB'``, ``'FG3M'``, ``'AST'``, ``'PF'``, ``'W_PCT'``, ``'VS_PLAYER_ID'``, ``'FG3_PCT'``, ``'PFD'``, ``'TEAM_NAME'``, ``'FG3A'``, ``'TOV'``, ``'TEAM_ID'``, ``'PLUS_MINUS'``, ``'VS_PLAYER_NAME'``

  ``'off-court'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'FTM'``, ``'TEAM_ABBREVIATION'``, ``'L'``, ``'W'``, ``'FGM'``, ``'OREB'``, ``'STL'``, ``'COURT_STATUS'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'DREB'``, ``'FG3M'``, ``'AST'``, ``'PF'``, ``'W_PCT'``, ``'VS_PLAYER_ID'``, ``'FG3_PCT'``, ``'PFD'``, ``'TEAM_NAME'``, ``'FG3A'``, ``'TOV'``, ``'TEAM_ID'``, ``'PLUS_MINUS'``, ``'VS_PLAYER_NAME'``

    

.. _request-team-rebounding:

team-rebounding
-------------------------------


Required Parameters:
  :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'overall'``
    ``'UC_DREB'``, ``'C_REB'``, ``'UC_REB_PCT'``, ``'C_DREB'``, ``'DREB'``, ``'G'``, ``'TEAM_NAME'``, ``'UC_REB'``, ``'C_REB_PCT'``, ``'C_OREB'``, ``'TEAM_ID'``, ``'REB_FREQUENCY'``, ``'OVERALL'``, ``'UC_OREB'``

  ``'shot-type'``
    ``'UC_DREB'``, ``'C_REB'``, ``'C_DREB'``, ``'UC_REB_PCT'``, ``'DREB'``, ``'G'``, ``'TEAM_NAME'``, ``'C_OREB'``, ``'UC_REB'``, ``'C_REB_PCT'``, ``'SHOT_TYPE_RANGE'``, ``'TEAM_ID'``, ``'UC_OREB'``, ``'SORT_ORDER'``

  ``'contesting-rebounders'``
    ``'UC_DREB'``, ``'C_REB'``, ``'C_DREB'``, ``'UC_REB_PCT'``, ``'DREB'``, ``'G'``, ``'TEAM_NAME'``, ``'UC_REB'``, ``'C_REB_PCT'``, ``'C_OREB'``, ``'TEAM_ID'``, ``'UC_OREB'``, ``'SORT_ORDER'``, ``'REB_NUM_CONTESTING_RANGE'``, ``'REB_FREQUENCY'``, ``'REB'``

  ``'shot-distance'``
    ``'UC_DREB'``, ``'C_REB'``, ``'SHOT_DIST_RANGE'``, ``'C_DREB'``, ``'UC_REB_PCT'``, ``'DREB'``, ``'G'``, ``'TEAM_NAME'``, ``'UC_REB'``, ``'C_REB_PCT'``, ``'C_OREB'``, ``'TEAM_ID'``, ``'UC_OREB'``

  ``'rebound-distance'``
    ``'UC_DREB'``, ``'C_REB'``, ``'C_DREB'``, ``'UC_REB_PCT'``, ``'DREB'``, ``'G'``, ``'TEAM_NAME'``, ``'REB_DIST_RANGE'``, ``'UC_REB'``, ``'C_REB_PCT'``, ``'C_OREB'``, ``'TEAM_ID'``, ``'UC_OREB'``

    

.. _request-team-roster:

team-roster
-------------------------------


Required Parameters:
  :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`LeagueID <param-leagueid>`

Return Fields:
  ``'players'``
    ``'SCHOOL'``, ``'HEIGHT'``, ``'WEIGHT'``, ``'TeamID'``, ``'EXP'``, ``'PLAYER_ID'``, ``'AGE'``, ``'PLAYER'``, ``'NUM'``, ``'LeagueID'``

  ``'coaches'``
    ``'COACH_NAME'``, ``'COACH_CODE'``, ``'TEAM_ID'``, ``'SCHOOL'``, ``'COACH_ID'``, ``'SORT_SEQUENCE'``, ``'LAST_NAME'``

    

.. _request-team-season-stats:

team-season-stats
-------------------------------


Required Parameters:
  :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`MeasureType <param-measuretype>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`PaceAdjust <param-paceadjust>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`PlusMinus <param-plusminus>`, :ref:`Rank <param-rank>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'overall'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'FTM'``, ``'L'``, ``'W'``, ``'GROUP_SET'``, ``'GROUP_VALUE'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'DREB'``, ``'FG3M'``, ``'AST'``, ``'PF'``, ``'BLKA'``, ``'FG3_PCT'``, ``'PFD'``, ``'TEAM_NAME'``, ``'FG3A'``, ``'TOV'``, ``'TEAM_ID'``, ``'PLUS_MINUS'``

  ``'player-totals'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'L'``, ``'W'``, ``'GROUP_SET'``, ``'DD2'``, ``'STL'``, ``'PF'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'DREB'``, ``'FG3M'``, ``'AST'``, ``'TD3'``, ``'BLKA'``, ``'FG3_PCT'``, ``'PFD'``, ``'FTM'``, ``'PLAYER_NAME'``, ``'FG3A'``, ``'TOV'``, ``'PLAYER_ID'``, ``'PLUS_MINUS'``, ``'OREB'``, ``'MIN'``, ``'FG_PCT'``, ``'REB'``, ``'W_PCT'``

    

.. _request-team-shooting:

team-shooting
-------------------------------


Required Parameters:
  :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'general'``
    ``'FG3M'``, ``'FGA_FREQUENCY'``, ``'SHOT_TYPE'``, ``'G'``, ``'TEAM_NAME'``, ``'FG3_PCT'``, ``'FG3A_FREQUENCY'``, ``'FG2M'``, ``'FG3A'``, ``'FGA'``, ``'EFG_PCT'``, ``'FG2A_FREQUENCY'``, ``'SORT_ORDER'``, ``'FG2_PCT'``, ``'FG2A'``, ``'FG_PCT'``, ``'FGM'``

  ``'shot-clock'``
    ``'FG2M'``, ``'FGA_FREQUENCY'``, ``'G'``, ``'TEAM_NAME'``, ``'FG3_PCT'``, ``'FG3A_FREQUENCY'``, ``'FG3M'``, ``'FG3A'``, ``'SHOT_CLOCK_RANGE'``, ``'EFG_PCT'``, ``'FG2A_FREQUENCY'``, ``'SORT_ORDER'``, ``'FG2_PCT'``

  ``'dribble'``
    ``'FG3M'``, ``'FGA_FREQUENCY'``, ``'G'``, ``'TEAM_NAME'``, ``'FG3_PCT'``, ``'FG3A_FREQUENCY'``, ``'FG2M'``, ``'DRIBBLE_RANGE'``, ``'FG3A'``, ``'FGA'``, ``'EFG_PCT'``, ``'FG2A_FREQUENCY'``, ``'SORT_ORDER'``

  ``'closest-defender'``
    ``'FG3M'``, ``'FGA_FREQUENCY'``, ``'G'``, ``'TEAM_NAME'``, ``'FG3_PCT'``, ``'CLOSE_DEF_DIST_RANGE'``, ``'FG3A_FREQUENCY'``, ``'FG2M'``, ``'FG3A'``, ``'FGA'``, ``'EFG_PCT'``, ``'FG2A_FREQUENCY'``, ``'SORT_ORDER'``, ``'FG2_PCT'``, ``'FG2A'``, ``'FG_PCT'``, ``'FGM'``

  ``'closest-defender-10ft'``
    ``'FG3M'``, ``'FGA_FREQUENCY'``, ``'G'``, ``'TEAM_NAME'``, ``'FG3_PCT'``, ``'CLOSE_DEF_DIST_RANGE'``, ``'FG3A_FREQUENCY'``, ``'FG2M'``, ``'FG3A'``, ``'FGA'``, ``'EFG_PCT'``, ``'FG2A_FREQUENCY'``, ``'SORT_ORDER'``, ``'FG2_PCT'``, ``'FG2A'``, ``'FG_PCT'``, ``'FGM'``

  ``'touch-time'``
    ``'FG3M'``, ``'FGA_FREQUENCY'``, ``'G'``, ``'TEAM_NAME'``, ``'FG3_PCT'``, ``'TOUCH_TIME_RANGE'``, ``'FG3A_FREQUENCY'``, ``'FG2M'``, ``'FG3A'``, ``'FGA'``, ``'EFG_PCT'``, ``'FG2A_FREQUENCY'``, ``'SORT_ORDER'``

    

.. _request-team-shooting-splits:

team-shooting-splits
-------------------------------


Required Parameters:
  :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`MeasureType <param-measuretype>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`PaceAdjust <param-paceadjust>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`PlusMinus <param-plusminus>`, :ref:`Rank <param-rank>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'overall'``
    ``'PCT_AST_3PM'``, ``'FG3M'``, ``'PCT_AST_FGM'``, ``'CFPARAMS'``, ``'BLKA'``, ``'PCT_UAST_2PM'``, ``'PCT_UAST_FGM'``, ``'FG_PCT'``, ``'FG3A'``, ``'GROUP_VALUE'``, ``'EFG_PCT'``, ``'GROUP_SET'``, ``'FGA'``, ``'PCT_AST_2PM'``, ``'CFID'``, ``'PCT_UAST_3PM'``, ``'FG3_PCT'``

  ``'shot-5ft'``
    ``'PCT_AST_3PM'``, ``'FG3M'``, ``'PCT_AST_FGM'``, ``'CFPARAMS'``, ``'BLKA'``, ``'PCT_UAST_2PM'``, ``'PCT_UAST_FGM'``, ``'FG_PCT'``, ``'FG3A'``, ``'GROUP_VALUE'``, ``'EFG_PCT'``, ``'GROUP_SET'``, ``'FGA'``, ``'PCT_AST_2PM'``, ``'CFID'``, ``'PCT_UAST_3PM'``, ``'FG3_PCT'``

  ``'shot-8ft'``
    ``'PCT_AST_3PM'``, ``'FG3M'``, ``'PCT_AST_FGM'``, ``'CFPARAMS'``, ``'BLKA'``, ``'PCT_UAST_2PM'``, ``'PCT_UAST_FGM'``, ``'FG_PCT'``, ``'FG3A'``, ``'GROUP_VALUE'``, ``'EFG_PCT'``, ``'GROUP_SET'``, ``'FGA'``, ``'PCT_AST_2PM'``, ``'CFID'``, ``'PCT_UAST_3PM'``, ``'FG3_PCT'``

  ``'shot-area'``
    ``'PCT_AST_3PM'``, ``'FG3M'``, ``'PCT_AST_FGM'``, ``'CFPARAMS'``, ``'BLKA'``, ``'PCT_UAST_2PM'``, ``'PCT_UAST_FGM'``, ``'FG_PCT'``, ``'FG3A'``, ``'GROUP_VALUE'``, ``'EFG_PCT'``, ``'GROUP_SET'``, ``'FGA'``, ``'PCT_AST_2PM'``, ``'CFID'``, ``'PCT_UAST_3PM'``, ``'FG3_PCT'``

  ``'assisted-shot'``
    ``'PCT_AST_3PM'``, ``'FG3M'``, ``'PCT_AST_FGM'``, ``'CFPARAMS'``, ``'BLKA'``, ``'PCT_UAST_2PM'``, ``'PCT_UAST_FGM'``, ``'FG_PCT'``, ``'FG3A'``, ``'GROUP_VALUE'``, ``'EFG_PCT'``, ``'GROUP_SET'``, ``'FGA'``, ``'PCT_AST_2PM'``, ``'CFID'``, ``'PCT_UAST_3PM'``, ``'FG3_PCT'``

  ``'shot-type'``
    ``'PCT_AST_3PM'``, ``'FG3M'``, ``'PCT_AST_FGM'``, ``'CFPARAMS'``, ``'BLKA'``, ``'PCT_UAST_2PM'``, ``'PCT_UAST_FGM'``, ``'FG_PCT'``, ``'FG3A'``, ``'GROUP_VALUE'``, ``'EFG_PCT'``, ``'GROUP_SET'``, ``'FGA'``, ``'PCT_AST_2PM'``, ``'CFID'``, ``'PCT_UAST_3PM'``, ``'FG3_PCT'``

  ``'assisted-by'``
    ``'PCT_AST_3PM'``, ``'FG3M'``, ``'PCT_AST_FGM'``, ``'CFPARAMS'``, ``'BLKA'``, ``'PCT_UAST_2PM'``, ``'PCT_UAST_FGM'``, ``'FG_PCT'``, ``'PLAYER_NAME'``, ``'FG3A'``, ``'EFG_PCT'``, ``'PLAYER_ID'``, ``'FGM'``, ``'FGA'``, ``'PCT_AST_2PM'``, ``'CFID'``, ``'PCT_UAST_3PM'``

    

.. _request-team-splits:

team-splits
-------------------------------


Required Parameters:
  :ref:`Season <param-season>`, :ref:`TeamID <param-teamid>`

Optional Parameters:
  :ref:`DateFrom <param-datefrom>`, :ref:`DateTo <param-dateto>`, :ref:`GameSegment <param-gamesegment>`, :ref:`LastNGames <param-lastngames>`, :ref:`LeagueID <param-leagueid>`, :ref:`Location <param-location>`, :ref:`MeasureType <param-measuretype>`, :ref:`Month <param-month>`, :ref:`OpponentTeamID <param-opponentteamid>`, :ref:`Outcome <param-outcome>`, :ref:`PaceAdjust <param-paceadjust>`, :ref:`Period <param-period>`, :ref:`PerMode <param-permode>`, :ref:`PlusMinus <param-plusminus>`, :ref:`Rank <param-rank>`, :ref:`SeasonSegment <param-seasonsegment>`, :ref:`SeasonType <param-seasontype>`, :ref:`VsConference <param-vsconference>`, :ref:`VsDivision <param-vsdivision>`

Return Fields:
  ``'overall'``
    ``'SEASON_YEAR'``, ``'PTS'``, ``'GP'``, ``'L'``, ``'W'``, ``'GROUP_SET'``, ``'GROUP_VALUE'``, ``'BLK'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'CFPARAMS'``, ``'DREB'``, ``'FG3M'``, ``'CFID'``, ``'AST'``, ``'PF'``, ``'BLKA'``, ``'FG3_PCT'``, ``'PFD'``, ``'FTM'``, ``'FG3A'``, ``'TOV'``, ``'PLUS_MINUS'``, ``'OREB'``, ``'MIN'``, ``'FG_PCT'``, ``'REB'``, ``'W_PCT'``

  ``'location'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'L'``, ``'W'``, ``'GROUP_SET'``, ``'GROUP_VALUE'``, ``'TEAM_GAME_LOCATION'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'CFPARAMS'``, ``'DREB'``, ``'FG3M'``, ``'CFID'``, ``'AST'``, ``'TOV'``, ``'BLKA'``, ``'FG3_PCT'``, ``'PFD'``, ``'FTM'``, ``'FG3A'``, ``'PF'``, ``'PLUS_MINUS'``, ``'OREB'``, ``'MIN'``, ``'FG_PCT'``, ``'REB'``

  ``'wins-losses'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'L'``, ``'W'``, ``'GROUP_SET'``, ``'GROUP_VALUE'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'CFPARAMS'``, ``'DREB'``, ``'FG3M'``, ``'CFID'``, ``'AST'``, ``'PF'``, ``'BLKA'``, ``'FG3_PCT'``, ``'PFD'``, ``'FTM'``, ``'FG3A'``, ``'TOV'``, ``'GAME_RESULT'``, ``'PLUS_MINUS'``, ``'OREB'``, ``'MIN'``, ``'FG_PCT'``

  ``'month'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'L'``, ``'W'``, ``'GROUP_SET'``, ``'GROUP_VALUE'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'CFPARAMS'``, ``'DREB'``, ``'FG3M'``, ``'CFID'``, ``'AST'``, ``'PF'``, ``'BLKA'``, ``'FG3_PCT'``, ``'PFD'``, ``'FTM'``, ``'FG3A'``, ``'TOV'``, ``'PLUS_MINUS'``, ``'OREB'``, ``'MIN'``, ``'FG_PCT'``, ``'REB'``, ``'W_PCT'``

  ``'pre-post-allstar'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'FTA'``, ``'L'``, ``'W'``, ``'GROUP_SET'``, ``'GROUP_VALUE'``, ``'STL'``, ``'FGA'``, ``'FT_PCT'``, ``'SEASON_SEGMENT'``, ``'CFPARAMS'``, ``'DREB'``, ``'FG3M'``, ``'CFID'``, ``'AST'``, ``'PF'``, ``'BLKA'``, ``'FG3_PCT'``, ``'PFD'``, ``'FTM'``, ``'FG3A'``, ``'TOV'``, ``'PLUS_MINUS'``, ``'OREB'``, ``'MIN'``, ``'FG_PCT'``, ``'REB'``

  ``'days-rest'``
    ``'BLK'``, ``'PTS'``, ``'GP'``, ``'L'``, ``'W'``, ``'GROUP_SET'``, ``'GROUP_VALUE'``, ``'STL'``, ``'TEAM_DAYS_REST_RANGE'``, ``'FGA'``, ``'FT_PCT'``, ``'FTA'``, ``'CFPARAMS'``, ``'DREB'``, ``'FG3M'``, ``'CFID'``, ``'AST'``, ``'PF'``, ``'BLKA'``, ``'FG3_PCT'``, ``'PFD'``, ``'FTM'``, ``'FG3A'``, ``'TOV'``, ``'PLUS_MINUS'``, ``'OREB'``, ``'MIN'``, ``'FG_PCT'``, ``'REB'``

    

**********
Parameters
**********

.. _param-aheadbehind:

AheadBehind
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``'Ahead or Behind'``, ``'Behind or Tied'``, ``'Ahead or Tied'``

Default:
``Ahead or Behind``

.. _param-clutchtime:

ClutchTime
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``, ``'Last 5 Minutes'``, ``'Last 4 Minutes'``, ``'Last 3 Minutes'``, ``'Last 2 Minutes'``, ``'Last 1 Minute'``, ``'Last 30 Seconds'``, ``'Last 10 Seconds'``

Default:
``''``

.. _param-contextfilter:

ContextFilter
---------------------
Honestly don't know what the format of this argument should be, but there's a request that requires it so it defaults to always empty.

Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``

Default:
``''``

.. _param-contextmeasure:

ContextMeasure
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``'FGM'``, ``'FGA'``, ``'PG_PCT'``, ``'FG3M'``, ``'FG3A'``, ``'FG3_PCT'``, ``'PF'``, ``'EFG_PCT'``, ``'TS_PCT'``, ``'PTS_FB'``, ``'PTS_OFF_TOV'``, ``'PTS_2ND_CHANCE'``, ``'PF'``

Default:
``FGM``

.. _param-datefrom:

DateFrom
---------------------


Type:
  :ref:`Date <type-date>`

Default:
``''``

.. _param-dateto:

DateTo
---------------------


Type:
  :ref:`Date <type-date>`

Default:
``''``

.. _param-direction:

Direction
---------------------
Sort ascending or descending.

Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``'ASC'``, ``'DESC'``

Default:
``DESC``

.. _param-distancerange:

DistanceRange
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``, ``'5ft Range'``, ``'8ft Range'``, ``'By Zone'``

Default:
``''``

.. _param-endperiod:

EndPeriod
---------------------


Type:
  :ref:`Integer <type-integer>`

Default:
``10``

.. _param-endrange:

EndRange
---------------------


Type:
  :ref:`Integer <type-integer>`

Default:
``28800``

.. _param-gameid:

GameID
---------------------


Type:
  :ref:`Integer <type-integer>`


.. _param-gamescope:

GameScope
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``, ``'Yesterday'``, ``'Last 10'``

Default:
``''``

.. _param-gamesegment:

GameSegment
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``, ``'First Half'``, ``'Second Half'``, ``'Overtime'``

Default:
``''``

.. _param-groupquantity:

GroupQuantity
---------------------


Type:
  :ref:`Integer <type-integer>`

Default:
``5``

.. _param-isonlycurrentseason:

IsOnlyCurrentSeason
---------------------


Type:
  :ref:`Boolean <type-boolean>`

Default:
``False``

.. _param-lastngames:

LastNGames
---------------------


Type:
  :ref:`Integer <type-integer>`

Default:
``''``

.. _param-leagueid:

LeagueID
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``'NBA'``, ``'NBADL'``, ``'WNBA'``

Default:
``NBA``

.. _param-location:

Location
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``, ``'Home'``, ``'Road'``

Default:
``''``

.. _param-measuretype:

MeasureType
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``'Base'``, ``'Advanced'``, ``'Misc'``, ``'Four Factors'``, ``'Scoring'``, ``'Opponent'``, ``'Usage'``

Default:
``Base``

.. _param-month:

Month
---------------------


Type:
  :ref:`Integer <type-integer>`

Default:
``''``

.. _param-opponentteamid:

OpponentTeamID
---------------------


Type:
  :ref:`Integer <type-integer>`

Default:
``''``

.. _param-outcome:

Outcome
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``, ``'W'``, ``'L'``

Default:
``''``

.. _param-paceadjust:

PaceAdjust
---------------------


Type:
  :ref:`Boolean <type-boolean>`

Default:
``False``

.. _param-permode:

PerMode
---------------------
Whether returned stats should be given as totals, per game, per 36 minutes, etc. Some requests may not accept all values of this argument, however "Totals" and "PerGame" are always permitted.

Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``'Totals'``, ``'PerGame'``, ``'MinutesPer'``, ``'Per48'``, ``'Per40'``, ``'Per36'``, ``'PerMinute'``, ``'PerPossession'``, ``'PerPlay'``, ``'Per100Possessions'``, ``'Per100Plays'``

Default:
``Totals``

.. _param-period:

Period
---------------------


Type:
  :ref:`Integer <type-integer>`

Default:
``''``

.. _param-playerexperience:

PlayerExperience
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``, ``'Rookie'``, ``'Sophomore'``, ``'Veteran'``

Default:
``''``

.. _param-playerid:

PlayerID
---------------------


Type:
  :ref:`Integer <type-integer>`


.. _param-playerorteam:

PlayerOrTeam
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``, ``'P'``, ``'T'``

Default:
``T``

.. _param-playerposition:

PlayerPosition
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``, ``'F'``, ``'C'``, ``'G'``, ``'C-F'``, ``'F-C'``, ``'F-G'``, ``'G-F'``

Default:
``''``

.. _param-plusminus:

PlusMinus
---------------------


Type:
  :ref:`Boolean <type-boolean>`

Default:
``False``

.. _param-pointdiff:

PointDiff
---------------------


Type:
  :ref:`Integer <type-integer>`

Default:
``''``

.. _param-position:

Position
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``, ``'Guard'``, ``'Center'``, ``'Forward'``

Default:
``''``

.. _param-rangetype:

RangeType
---------------------


Type:
  :ref:`Integer <type-integer>`

Default:
``2``

.. _param-rank:

Rank
---------------------


Type:
  :ref:`Boolean <type-boolean>`

Default:
``False``

.. _param-rookieyear:

RookieYear
---------------------
(Guess) Include only players with the given rookie year?

Type:
  :ref:`Season <type-season>`

Default:
``''``

.. _param-scope:

Scope
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``, ``'RS'``, ``'S'``, ``'Rookies'``

Default:
``''``

.. _param-season:

Season
---------------------


Type:
  :ref:`Season <type-season>`


.. _param-seasonid:

SeasonID
---------------------
From the perspective of the user this is the same as :ref:`Season <param-season>`, though it is handled differently internally.

Type:
  :ref:`Season <type-season>`


.. _param-seasonsegment:

SeasonSegment
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``, ``'Post All-Star'``, ``'Pre All-Star'``

Default:
``''``

.. _param-seasontype:

SeasonType
---------------------
Some requests may not support pre-season.

Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``'Regular Season'``, ``'Playoffs'``, ``'All Star'``, ``'Pre Season'``

Default:
``Regular Season``

.. _param-seasonyear:

SeasonYear
---------------------
Same as :ref:`Season <param-season>`.

Type:
  :ref:`Season <type-season>`


.. _param-sorter:

Sorter
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``'MIN'``, ``'FGM'``, ``'FGA'``, ``'FG_PCT'``, ``'FG3M'``, ``'FG3A'``, ``'FF3_PCT'``, ``'FTM'``, ``'FTA'``, ``'FT_PCT'``, ``'OREB'``, ``'DREB'``, ``'REB'``, ``'AST'``, ``'STL'``, ``'BLK'``, ``'TOV'``, ``'PTS'``, ``'EFF'``

Default:
``PTS``

.. _param-startperiod:

StartPeriod
---------------------


Type:
  :ref:`Integer <type-integer>`

Default:
``1``

.. _param-startrange:

StartRange
---------------------


Type:
  :ref:`Integer <type-integer>`

Default:
``''``

.. _param-starterbench:

StarterBench
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``, ``'Starters'``, ``'Bench'``

Default:
``''``

.. _param-statcategory:

StatCategory
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``'MIN'``, ``'FGM'``, ``'FGA'``, ``'FG_PCT'``, ``'FG3M'``, ``'FG3A'``, ``'FF3_PCT'``, ``'FTM'``, ``'FTA'``, ``'FT_PCT'``, ``'OREB'``, ``'DREB'``, ``'REB'``, ``'AST'``, ``'STL'``, ``'BLK'``, ``'TOV'``, ``'PTS'``, ``'EFF'``

Default:
``PTS``

.. _param-teamid:

TeamID
---------------------


Type:
  :ref:`Integer <type-integer>`


.. _param-vsconference:

VsConference
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``, ``'East'``, ``'West'``

Default:
``''``

.. _param-vsdivision:

VsDivision
---------------------


Type:
  :ref:`Enumerated <type-enumerated>`

Options:
  ``''``, ``'Atlantic'``, ``'Central'``, ``'Northwest'``, ``'Pacific'``, ``'SouthEast'``, ``'SouthWest'``, ``'East'``, ``'West'``

Default:
``''``

.. _param-year:

Year
---------------------


Type:
  :ref:`Integer <type-integer>`


***************
Parameter Types
***************

.. _type-integer:

Integer
-------

Parameters of type Integer accept standard Python integers.

.. _type-boolean:

Boolean
-------

Parameters of type Enumerated accept standard Python boolean values ``True`` and
``False``.

.. _type-enumerated:

Enumerated
----------

Parameters of type Enumerated accept Python strings. Each parameter has a set
of string values that it allows as options, see documentation for the
particular parameter to see what those values are. Some enumerated parameters
allow empty strings; semantically this indicates that the parameter is left
unspecified.

.. _type-date:

Date
----

Parameters of type Date accept Python ``datetime.date`` objects.

.. _type-season:

Season
------

Parameters of type Season accept four digit integers (i.e., integers between
1000 and 9999). Values should correspond to the year that a season begins; for
example, the value 2008 indicates the 2008-2009 NBA season.