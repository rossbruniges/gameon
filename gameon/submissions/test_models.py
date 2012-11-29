import test_utils

from . import models

class EntryFeatureVideoUrlTests(test_utils.TestCase):
    def _repr(self, model):
        return ("Entry(video_url=%s)"
                ".get_entry_feature()" % repr(model.video_url))

    def assertIsEmpty(self, video_url):
        m = models.Entry(video_url=video_url)
        html = m.get_entry_feature()
        if html is not None:
            self.fail("Expected %s to return None, but got %s" %
                      (self._repr(m), repr(html)))
        
    def assertIsEmbed(self, video_url):
        m = models.Entry(video_url=video_url)
        html = m.get_entry_feature()
        prefix = ("Expected %s to return an <iframe> tag, but got " %
                  self._repr(m))
        if html is None:
            self.fail(prefix + "None")
        if not html.startswith("<iframe"):
            self.fail(prefix + repr(html))

    def test_is_none_when_video_url_is_not_allowed_1(self):
        self.assertIsEmpty(video_url="http://mysite.org/foo")

    def test_is_none_when_video_url_is_not_allowed_2(self):
        self.assertIsEmpty(video_url="http://mysite.org/youtube")

    def test_is_oembed_when_video_url_is_youtube_shorturl(self):
        self.assertIsEmbed(video_url="http://youtu.be/ITTxTCz4Ums")

    def test_is_oembed_when_video_url_is_youtube_longurl(self):
        self.assertIsEmbed(video_url="http://www.youtube.com/watch?v=ITTxTCz4Ums")

    def test_is_oembed_when_video_url_is_vimeo(self):
        self.assertIsEmbed(video_url="http://vimeo.com/42261942")
