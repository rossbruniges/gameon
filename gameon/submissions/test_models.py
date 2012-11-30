import test_utils

from . import models

class Url2EmbedTests(test_utils.TestCase):
    def test_falsy_value_returns_none(self):
        self.assertEqual(models.url2embed(None), None)
        
    def test_arbitrary_url_returns_none(self):
        self.assertEqual(models.url2embed("http://foo.org/blah"), None)

    def test_vimeo_url_works(self):
        self.assertEqual(models.url2embed("http://vimeo.com/channels/staffpicks/34062273"),
                         '<iframe src="https://player.vimeo.com/video/34062273?title=0&amp;byline=0&amp;portrait=0&amp;badge=0" width="640" height="385" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>')

    def test_short_youtube_url_works(self):
        self.assertEqual(models.url2embed("http://youtu.be/ITTxTCz4Ums"),
                         '<iframe class="youtube-player" type="text/html" width="640" height="385" src="https://www.youtube.com/embed/ITTxTCz4Ums" frameborder="0"></iframe>')

    def test_long_youtube_url_works(self):
        self.assertEqual(models.url2embed("http://www.youtube.com/watch?v=ITTxTCz4Ums"),
                         '<iframe class="youtube-player" type="text/html" width="640" height="385" src="https://www.youtube.com/embed/ITTxTCz4Ums" frameborder="0"></iframe>')
    
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
