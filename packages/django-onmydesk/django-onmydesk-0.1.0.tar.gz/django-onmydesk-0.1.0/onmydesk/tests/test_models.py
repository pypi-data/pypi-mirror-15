import base64
import pickle
from datetime import datetime, date
from decimal import Decimal, getcontext
from django.test import TestCase
from unittest import mock
from django import forms
from django.contrib.auth.models import User

from onmydesk.models import (Report, Scheduler, ReportNotSavedException,
                             output_file_handler)


class OutputFileHandlerTestCase(TestCase):

    def test_call_must_return_filepath_changed(self):
        my_handler = 'path.to.my.handler'
        with mock.patch('onmydesk.models.app_settings.ONMYDESK_FILE_HANDLER', my_handler):
            my_handler_mocked = mock.MagicMock(return_value='/tmp/filepath-changed.tsv')
            with mock.patch('onmydesk.models.my_import', return_value=my_handler_mocked) as my_import_mocked:
                self.assertEqual(
                    output_file_handler('/tmp/filepath.tsv'),
                    '/tmp/filepath-changed.tsv')

        my_import_mocked.assert_called_once_with(my_handler)
        my_handler_mocked.assert_called_once_with('/tmp/filepath.tsv')

    def test_call_must_return_same_filepath_if_a_file_handler_not_exists(self):
        with mock.patch('onmydesk.models.ONMYDESK_FILE_HANDLER', None):
            self.assertEqual(output_file_handler('/tmp/filepath.tsv'), '/tmp/filepath.tsv')


class ReportTestCase(TestCase):

    def setUp(self):
        def my_output_file_handler(filepath):
            return filepath

        self.patch('onmydesk.models.output_file_handler', my_output_file_handler)

        self.report_instance = mock.MagicMock()
        self.report_instance.name = 'My Report'
        self.report_instance.output_filepaths = ['/tmp/flunfa.tsv']

        self.report_class = mock.MagicMock(return_value=self.report_instance)
        self.report_class.name = 'My Report'

        self.my_import_mocked = self.patch('onmydesk.models.my_import', return_value=self.report_class)

    def test_to_string(self):
        report = Report(report='my_report_class')
        self.assertEqual(str(report), self.report_instance.name)

        report.save()

        self.assertEqual(str(report), '{} #{}'.format(self.report_instance.name, report.id))

    def test_to_string_with_empty_report_must_return_generic_name(self):
        report = Report()
        self.assertEqual(str(report), 'Report object')

    def test_process_must_call_process_from_report_class(self):
        report = Report(report='my_report_class')
        report.save()
        report.process()

        self.my_import_mocked.assert_called_once_with(report.report)
        self.assertTrue(self.report_instance.process.called)

    def test_process_with_not_saved_report_must_raise_a_exception(self):
        report = Report(report='my_report_class')
        self.assertRaises(ReportNotSavedException, report.process)

    def test_process_must_store_filepaths_result(self):
        self.report_instance.output_filepaths = [
            '/tmp/flunfa-2.tsv',
            '/tmp/flunfa-3.tsv',
        ]

        report = Report(report='my_report_class')
        report.save()
        report.process()

        self.assertEqual(
            report.results, ';'.join(self.report_instance.output_filepaths))

    def test_process_with_params_must_call_report_constructor_with_these_params(self):
        report = Report(report='my_report_class')

        params = {'type': 'whatever'}

        report.set_params(params)
        report.save()

        report.process()

        self.report_class.assert_called_once_with(params=params)

    def test_process_must_set_status_as_processing_when_start(self):
        self.patch('onmydesk.models.my_import', side_effect=Exception)

        report = Report(report='my_report_class')
        report.save()

        self.assertEqual(report.status, Report.STATUS_PENDING)

        try:
            report.process()
        except Exception:
            pass

        report = Report.objects.get(id=report.id)
        self.assertEqual(report.status, Report.STATUS_PROCESSING)

    def test_process_must_set_status_as_processed_after_report_process(self):
        report = Report(report='my_report_class')
        report.save()
        report.process()

        report = Report.objects.get(id=report.id)
        self.assertEqual(report.status, Report.STATUS_PROCESSED)

    def test_process_must_set_status_as_error_if_some_exception_is_raised(self):
        self.report_instance.process.side_effect = Exception()

        report = Report(report='my_report_class')
        report.save()

        self.assertRaises(Exception, report.process)
        self.assertEqual(report.status, Report.STATUS_ERROR)

    def test_process_must_set_process_time(self):
        getcontext().prec = 5
        start = Decimal(10.0000)
        end = Decimal(15.1234)
        self.patch('onmydesk.models.timer', side_effect=[start, end])

        report = Report(report='my_report_class')
        report.save()
        report.process()

        self.assertEqual(report.process_time, end - start)

    def test_results_as_list_must_return_a_list(self):
        expected_results = [
            '/tmp/flunfa-2.tsv',
            '/tmp/flunfa-3.tsv',
        ]

        report = Report(report='my_report_class')
        report.results = ';'.join(expected_results)

        self.assertEqual(report.results_as_list, expected_results)

    def test_results_as_list_must_return_empty_list_if_field_is_empty(self):
        report = Report(report='my_report_class')
        report.results = ''

        self.assertEqual(report.results_as_list, [])

    def test_set_params_must_serializer_info_and_store_on_params_attr(self):
        report = Report(report='my_report_class')

        self.assertIsNone(report.params)

        params = {'param1': 1, 'somedate': datetime.now()}
        expected_result = base64.b64encode(pickle.dumps(params))

        report.set_params(params)

        self.assertEqual(report.params, expected_result)

    def test_get_params_must_return_unserialized_info(self):
        params = {'param1': 1, 'somedate': datetime.now()}

        report = Report(report='my_report_class')
        report.params = base64.b64encode(pickle.dumps(params))

        self.assertEqual(report.get_params(), params)

    def test_get_params_returns_none_if_params_is_none(self):
        report = Report(report='my_report_class')
        report.params = None

        self.assertIsNone(report.get_params())

    @mock.patch('onmydesk.models.app_settings.ONMYDESK_DOWNLOAD_LINK_HANDLER', 'whatever')
    def test_result_links(self):
        self.report_instance.output_filepaths = [
            '/tmp/flunfa-2.tsv',
            '/tmp/flunfa-3.tsv',
        ]

        report = Report(report='my_report_class')

        report.save()
        report.process()

        def my_handler(filepath):
            url_example = 'http://someplace.com/somepath{}'
            return url_example.format(filepath)

        with mock.patch('onmydesk.models.my_import', return_value=my_handler):
            links = report.result_links
            self.assertEqual(links, [my_handler(i) for i in self.report_instance.output_filepaths])

    def patch(self, *args, **kwargs):
        patcher = mock.patch(*args, **kwargs)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing


class SchedulerTestCase(TestCase):

    def setUp(self):
        class RangeDateForm(forms.Form):
            my_date = forms.DateField()
            other_filter = forms.CharField()

        self.report_form = RangeDateForm

        self.report_class = mock.MagicMock()
        self.report_class.form = self.report_form
        self.report_class.get_form.return_value = self.report_form
        self.report_class.name = 'My Report'

        self._patch('onmydesk.models.my_import', return_value=self.report_class)

    def _patch(self, *args, **kwargs):
        patcher = mock.patch(*args, **kwargs)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_to_string(self):

        scheduler = Scheduler(report='my_report_class')

        with mock.patch('onmydesk.models.my_import', return_value=self.report_class):
            self.assertEqual(str(scheduler), 'My Report')

            scheduler.save()
            self.assertEqual(str(scheduler), 'My Report #{}'.format(scheduler.id))

    def test_to_string_with_empty_report_returns_generic_name(self):
        scheduler = Scheduler()

        self.assertEqual(str(scheduler), 'Scheduler object')

    def test_set_params_must_serializer_info_and_store_on_params_attr(self):
        scheduler = Scheduler()

        params = {'teste': 'Alisson'}

        scheduler.set_params(params)

        expected_result = base64.b64encode(pickle.dumps(params))
        self.assertEqual(scheduler.params, expected_result)

    def test_get_params_must_return_unserialized_info(self):
        params = {'param1': 1}

        report = Scheduler()
        report.params = base64.b64encode(pickle.dumps(params))

        self.assertEqual(report.get_params(), params)

    def test_get_processed_params_must_return_dictionary_with_parameters(self):
        scheduler = Scheduler()

        params = {'param1': 'First value'}

        scheduler.set_params(params)

        self.assertEqual(scheduler.get_processed_params(), params)

    def test_get_processed_params_must_return_date_fields_processed(self):
        scheduler = Scheduler(report='my_report_class')
        scheduler.set_params({'my_date': 'D-2', 'other_filter': 'other_value'})

        reference_date = date(2016, 4, 3)
        expected_param = {'my_date': date(2016, 4, 1), 'other_filter': 'other_value'}
        self.assertEqual(scheduler.get_processed_params(reference_date), expected_param)

    def test_get_processed_params_must_return_none_if_params_is_none(self):
        scheduler = Scheduler(report='my_report_class')
        scheduler.params = None

        self.assertIsNone(scheduler.get_processed_params())

    def test_process_must_return_report(self):
        scheduler = Scheduler(report='my_report_class')
        result = scheduler.process()

        self.assertIsInstance(result, Report)

    def test_process_must_return_a_saved_report(self):
        scheduler = Scheduler(report='my_report_class')
        report = scheduler.process()

        self.assertIsNotNone(report.id)

    def test_process_must_return_a_saved_report_with_created_by_filled(self):
        user = User.objects.create_user('Joao', 'joao.webmaster@webnastersonline.com.br', '123souwebmaster')
        scheduler = Scheduler(report='my_report_class', created_by=user)

        report = scheduler.process()

        self.assertEqual(report.created_by, user)

    def test_process_must_call_report_process(self):
        scheduler = Scheduler(report='my_report_class')

        with mock.patch('onmydesk.models.Report.process') as process_mocked:
            scheduler.process()
            self.assertTrue(process_mocked.called)

    def test_process_must_notify_users(self):
        scheduler = Scheduler(report='my_report_class', notify_emails='test@test.com,other@test.com')

        with mock.patch('onmydesk.models.send_mail') as send_mail_mocked:
            scheduler.process()
            self.assertTrue(send_mail_mocked.called)

    def test_process_must_not_notify_if_scheduler_has_no_emails(self):
        scheduler = Scheduler(report='my_report_class')

        with mock.patch('onmydesk.models.send_mail') as send_mail_mocked:
            scheduler.process()
            self.assertFalse(send_mail_mocked.called)

    def test_process_must_use_given_reference_date(self):
        self._patch('onmydesk.models.Report.process')

        scheduler = Scheduler(report='my_report_class')
        scheduler.set_params({'my_date': 'D-2', 'other_filter': 'other_value'})

        my_date = date(2016, 5, 10)
        with mock.patch('onmydesk.models.Report.set_params') as set_params:
            scheduler.process(reference_date=my_date)
            set_params.assert_called_once_with({'my_date': date(2016, 5, 8), 'other_filter': 'other_value'})
