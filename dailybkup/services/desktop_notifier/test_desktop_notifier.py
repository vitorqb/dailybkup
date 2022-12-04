import dailybkup.services.desktop_notifier as sut
import dailybkup.testutils as tu


class TestNotifySendNotifier:
    def test_calls_send_notify_with_proper_arguments(self):
        petition = sut.DesktopNotificationPetition("foo", "bar")
        with tu.mock_os_run() as os_run:
            notifier = sut.NotifySendNotifier(command="echo")
            notifier.send(petition)
            os_run.assert_called_once_with(["echo", "foo", "bar"])
