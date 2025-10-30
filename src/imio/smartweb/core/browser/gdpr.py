from imio.gdpr.browser.views import GDPRView as BaseGDPRView


class GDPRView(BaseGDPRView):
    hide_herobanner = True

    def __call__(self):
        return super(GDPRView, self).__call__()
