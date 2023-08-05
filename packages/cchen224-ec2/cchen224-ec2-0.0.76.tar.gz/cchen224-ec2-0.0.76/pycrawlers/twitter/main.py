import csv
import traceback
from random import random
from time import sleep

from cutils import Gmail
from cutils import ProgressBar

from webparser_tweet import parse_tweet
from webparser_user_info import parse_user_info


class TwitterCrawler:

    def __init__(self, job):
        self._job = job.lower()
        self._p_sleep = 0.999
        self._t_sleep = 10
        self._input_fp = ''
        self._output_fp = ''

        if 'info' in self._job.lower():
            self._extension = '.info'
        elif 'timeline' in self._job.lower():
            self._extension = '.timeline'
        elif 'threads' in self._job.lower():
            self._extension = '.threads'
        elif 'tweet' in self._job.lower():
            self._extension = '.tweet'

    def set_input(self, input, **kwargs):
        if isinstance(input, str):
            delimiter = kwargs.get('delimiter', ',')
            index = kwargs.get('index', [0])
            self._input_fp = input
            with open(input, 'r') as i:
                csvreader = csv.reader(i, delimiter=delimiter)
                self._input = [row[index] for row in csvreader]
        if isinstance(input, list):
            self._input = input
            self._input_fp = ''
        return self

    def set_output(self, output_fp, output_delimiter=','):
        self._output_fp = output_fp
        self._output_delimiter = output_delimiter
        return self

    def set_notifier(self, notifier_type, **kwargs):
        if 'gmail' in notifier_type.lower():
            credential_fp = kwargs.get('credential', './')
            self._notifier = Gmail() \
                .set_from_to() \
                .set_credentials(credential_fp) \
                .set_subject('AWS Twitter' + self._extension) \
                .send_message(self._input_fp + '\n\n\n')
            self._notifier_error = Gmail() \
                .set_from_to() \
                .set_credentials(credential_fp) \
                .set_subject('AWS Twitter' + self._extension + ' Error!') \
                .send_message(self._input_fp + '\n\n\n')
        return self

    def log(self, message, is_close=False):
        if isinstance(self._notifier, Gmail):
            self._notifier.send_message(message)
        if is_close:
            self._notifier.close()
            self._notifier.send_message(self._input_fp + '\n\n\n')

    def throw(self, message):
        if isinstance(self._notifier_error, Gmail):
            self._notifier_error.send_message(message).close()
            self._notifier_error.send_message(self._input_fp + '\n\n\n')

    def crawl(self):
        bar = ProgressBar(total=len(self._input))
        with open(self._output_fp if self._output_fp != '' else self._input_fp + self._extension, 'a') as o:
            csvwriter = csv.writer(o, delimiter = self._output_delimiter)
            print self._input_fp, ':'
            for item in self._input:
                bar.move().log()
                if random() > self._p_sleep:
                    t = random() * self._t_sleep
                    print 'Random sleeping', t, 'sec',
                    sleep(t)
                crawl_function = {'.info': parse_user_info(item),
                                  '.tweet': parse_tweet(item)}.get(self._extension)
                self.log(' ' + item + '...')
                try:
                    csvwriter.writerow(crawl_function)
                    self.log('Done.\n')
                # except KeyboardInterrupt:
                #     self.log('KeyboardInterrupt!\n', True)
                #     break
                except:
                    self.throw(self._input + ':user ' + item + '\n' + traceback.format_exc())
            self.log('\n\n' + '\nDone', True)
        bar.close()

    def record(self):
        self.log('KeyboardInterrupt!\n', True)
