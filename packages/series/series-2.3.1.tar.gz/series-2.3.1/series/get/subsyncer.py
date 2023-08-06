# -*- coding: utf-8 -*-

from datetime import datetime

import requests

from tek.config import configurable
from tek import logger
from tek.tools import datetime_to_unix

from series import subsync
from series.get.handler import ReleaseHandler
from series.subsync.errors import NoSubsForEpisode


@configurable(series=['series_dir'], get=['sub_exclude'])
class Subsyncer(ReleaseHandler):

    def __init__(self, releases, *a, **kw):
        super().__init__(releases, 60, 'subtitle downloader')

    def _qualify(self, monitor):
        return (monitor.release.name not in self._sub_exclude and
                monitor.archived and not monitor.subtitles_downloaded and
                monitor.retry_subtitle_download)

    def _handle(self, monitor):
        release = monitor.release
        text = 'Downloading subs for episode {!s}…'
        logger.info(text.format(release))
        try:
            sub = subsync.get_episode(release.name, release.season,
                                      release.episode)
        except NoSubsForEpisode as e:
            logger.error('Subsyncer: {}'.format(e))
            monitor.subtitle_failures += 1
            monitor.last_subtitle_failure = datetime_to_unix(datetime.now())
            self._commit()
        except requests.RequestException as e:
            logger.error('Subsyncer: {}'.format(e))
        else:
            self._write_sub(monitor, sub)

    def _write_sub(self, monitor, sub):
        try:
            sub.write()
        except IOError as e:
            logger.error('Subsyncer: {}'.format(e))
        else:
            monitor.subtitles_downloaded = True
            self._commit()
            logger.info('Successfully downloaded subtitles.')

__all__ = ['Subsyncer']
