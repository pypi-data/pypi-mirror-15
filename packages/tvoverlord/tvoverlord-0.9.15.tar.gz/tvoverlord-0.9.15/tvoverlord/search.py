import sys
import subprocess
import os
import platform
import concurrent.futures
from pprint import pprint as pp
import socket

from tvoverlord.util import U
from tvoverlord.search_providers import extratorrent
from tvoverlord.search_providers import bitsnoop
from tvoverlord.search_providers import kickass_to
from tvoverlord.search_providers import thepiratebay_sx


class SearchError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Search(object):
    def __init__(self):
        self.season = ''
        self.episode = ''
        self.show_name = ''

    def job(self, engine, search_string, season, episode):
        search = engine.Provider()
        search_results = search.search(search_string, season, episode)

        return search_results

    def search(self, search_string, season=False, episode=False):
        """
        Return an array of values:

        [
          [
            ['Title string', 'search url'],
            [head1, head2, head3, id],
            [head1-width, head2-width, head3-width],
            [head1-alignment, head2-alignment, head3-alignment]
          ],
          [
            [<column 1 data>, <column 2 data>, <column 3 data>, <id>],
            [<column 1 data>, <column 2 data>, <column 3 data>, <id>],
            # etc...
          ]
        ]
        """

        self.season = season
        self.episode = episode
        self.show_name = search_string

        msg = 'Searching for: {0:s}...'.format(search_string)
        msg = U.hi_color(msg, foreground=16, background=184)
        sys.stdout.write(msg)
        sys.stdout.flush()
        backspace = '\b' * len(msg)
        overwrite = ' ' * len(msg)

        header = [
            [search_string, ''],
            ['Name', 'Size', 'Date', 'Seeds', 'SE'],
            [0, 10, 12, 6, 2],
            ['<', '>', '<', '>', '<']]

        engines = [bitsnoop, extratorrent, thepiratebay_sx, kickass_to]
        # engines = [bitsnoop]

        socket.setdefaulttimeout(3.05)
        episodes = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            res = {executor.submit(self.job, engine, search_string, season, episode): engine for engine in engines}
            for future in concurrent.futures.as_completed(res):
                # something = res[future]
                results = future.result()
                episodes = episodes + results

        episodes.sort(key=lambda x: int(x[3]), reverse=True)  # sort by seeds

        print('%s%s' % (backspace, overwrite), end=' ')

        # return search_results
        return [header] + [episodes]

    def download(self, chosen_show, destination):
        """
        Pass the chosen show's data and destination to the providers
        download method and return the name of the file downloaded
        back to get-nzb.v2.py
        """

        downloaded_filename = ''
        if chosen_show.startswith("magnet:"):

            if platform.system() == 'Linux':
                isX = True if os.environ.get('DISPLAY') else False
                if isX:
                    app = 'xdg-open'
                else:
                    sys.exit('\nNon X usage is not supported')

                try:
                    subprocess.Popen([app, chosen_show])
                except OSError:
                    sys.exit('\nYou do not have a bittorent client installed')
            elif platform.system() == 'Darwin':
                subprocess.Popen(["open", "--background", chosen_show])
            else:
                unknown_system = platform.platform()
                sys.exit('\nUnknown system:', unknown_system)

        else:  # is a nzb file
            final_name = ''
            # only cleans name for tv show downloads
            if self.season and self.episode:
                final_name = '%s.%s.nzb' % (
                    self.show_name.replace(' ', '.'),
                    "S%sE%s" % (self.season.rjust(2, '0'),
                                self.episode.rjust(2, '0'))
                )
                print(final_name)
            downloaded_filename = self.engine.download(
                chosen_show, destination, final_name)

        return downloaded_filename


if __name__ == '__main__':
    test = Search('nzbindex')
    test = Search('NZBIndex')
    test = Search('x')
