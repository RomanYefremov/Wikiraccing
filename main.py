import random
import time
import wikipedia
from collections import deque
from typing import List
from main1 import db_summ

requests_per_minute = 100
links_per_page = 200


class WikiRacer:

    def find_path(self, start: str, finish: str) -> List[str]:
        wikipedia.set_lang('uk')
        try:
            page = wikipedia.page(start)
        except wikipedia.exceptions.DisambiguationError as ex:
            s = random.choice(ex.options)
            page = wikipedia.page(s)
        key = page.links
        graph = {start: key}
        queue = deque([start])
        visited = {finish: None}
        while queue:
            time.sleep(3)
            try:
                cure_node = queue.popleft()
                page = wikipedia.page(cure_node)
                links = page.links
                graph[cure_node] = links
                link_self = 0
                link_len = len(links)
                if cure_node in links:
                    link_self = 1
                db_summ(cure_node, link_self, link_len)
                if finish in links:
                    visited[finish] = cure_node
                    break
                else:
                    next_node = graph[cure_node]
                    for i in next_node:
                        if i not in queue:
                            queue.append(i)
                            visited[i] = cure_node

            except wikipedia.exceptions.PageError:
                continue
            except wikipedia.DisambiguationError as ex:
                continue
        path = []
        cure_node = finish
        while cure_node != start:
            cure_node = visited[cure_node]
            path.append(cure_node)
        path.reverse()
        path.append(finish)
        return path


if __name__ == '__main__':
    wiki = WikiRacer()
    a = wiki.find_path('Мітохондріальна ДНК', 'Вітамін K')
    print(a)
