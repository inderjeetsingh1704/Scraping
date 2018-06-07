# -*- coding: utf-8 -*-
import scrapy


class TeamSpider(scrapy.Spider):
    name = 'team'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/2018_FIFA_World_Cup_squads']
    
    def __init__(self,Team=None):
        self.team = Team
        
    def parse(self, response):
        if self.team:
            teams = response.xpath('//h3/span[@id="'+self.team+'"]/text()').extract()
        else:
            teams = response.xpath('//h3/span[@class="mw-headline"]/text()').extract()[:32]
        
        for team in teams:
            coach = response.xpath('//h3[span[@id="'+team+'"]]/following-sibling::p[1]/a/text()').extract_first()
            Squad = response.xpath('//h3[span[@id="'+team+'"]]/following-sibling::table[1]//tr')[1:]
            Squad_players = []
            for player in Squad:
                captain = False
                role=player.xpath('.//td[2]/a/text()').extract_first()
                playername = player.xpath('.//th//a/text()').extract()
                if len(playername)==2:
                    name = playername[0]
                    captain = True
                else:
                    name = playername[0]
                caps=player.xpath('.//td[4]/text()').extract_first()
                goals=player.xpath('.//td[5]/text()').extract_first()
                club_country = player.xpath('.//td[6]//a')[0].xpath('.//@title').extract_first()
                club_name =player.xpath('.//td[6]//a')[1].xpath('.//text()').extract_first()
                Player={
                    'Role':role,
                    'Player':{
                        'Name':name,
                        'Captain':captain
                    },
                    'International Caps':caps,
                    'International Goals':goals,
                    'Club':{
                        'Country':club_country,
                        'Name':club_name
                    }
                }
                Squad_players.append(Player)
                
            yield{
                'Team':team,
                'Coach':coach,
                'Squad':Squad_players
            }
            