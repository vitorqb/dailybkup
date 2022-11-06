import dailybkup.services.email_sender as sut
from dailybkup import testutils


class TestMailGunEmailSender:
    def test_send_success(self, wiremock: testutils.Wiremock):
        # ARRANGE
        wiremockRequest = wiremock.request(method="POST", url="/mailgun/messages")
        wiremockResponse = wiremock.response(status=200, json_body={})
        wiremock.stub(wiremockRequest, wiremockResponse)
        base_url = wiremock.url("/mailgun")
        petition = sut.EmailPetition(
            recipient_address="foo@bar.baz",
            subject="Subject",
            body="Body",
        )
        from_ = "DailyBkup <dailybkup@mail.com>"
        sender = sut.MailGunEmailSender(base_url=base_url, from_=from_, api_key="foo")

        # ACT
        sender.send(petition)

        # ASSERT
        request = wiremock.find(url="/mailgun/messages", method="POST")[0]
        assert request.formdata()["from"] == [from_]
        assert request.formdata()["to"] == [petition.recipient_address]
        assert request.formdata()["subject"] == [petition.subject]
        assert request.formdata()["text"] == [petition.body]
