# -*- coding: utf-8 -*-
'''
Viewers for configuration and generic actions

@author: Laurent GAY
@organization: sd-libre.fr
@contact: info@sd-libre.fr
@copyright: 2015 sd-libre.fr
@license: This file is part of Lucterios.

Lucterios is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lucterios is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lucterios.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import unicode_literals
from datetime import datetime
from _io import StringIO, TextIOWrapper
from csv import DictReader
from _csv import QUOTE_NONE, QUOTE_ALL
from copy import deepcopy

from django.utils.translation import ugettext_lazy as _
from django.utils import six
from django.core.exceptions import ObjectDoesNotExist
from django.apps.registry import apps
from django.db.models.fields import DateField
from django.db.models import Q

from lucterios.framework.tools import MenuManage, FORMTYPE_NOMODAL, FORMTYPE_REFRESH, CLOSE_NO, WrapAction, ActionsManage, \
    FORMTYPE_MODAL, get_icon_path, SELECT_SINGLE, CLOSE_YES
from lucterios.framework.xfergraphic import XferContainerCustom
from lucterios.framework.xferadvance import XferDelete, XferAddEditor, XferListEditor
from lucterios.framework.xfercomponents import XferCompImage, XferCompLabelForm, XferCompEdit, XferCompGrid, \
    XferCompSelect, XferCompUpLoad, XferCompButton
from lucterios.framework import signal_and_lock
from lucterios.framework.error import LucteriosException, IMPORTANT
from lucterios.CORE.models import LucteriosUser
from lucterios.CORE.views_usergroup import UsersEdit
from lucterios.CORE.xferprint import XferPrintAction
from lucterios.CORE.parameters import Params
from lucterios.contacts.models import PostalCode, Function, StructureType, LegalEntity, Individual, \
    CustomField, AbstractContact, Responsability
from lucterios.contacts.views_contacts import LegalEntityAddModify, \
    LegalEntityShow
from lucterios.framework.filetools import get_user_path, readimage_to_base64
from os.path import exists


@ActionsManage.affect('LegalEntity', 'currentmodify')
@MenuManage.describ(None)
class CurrentLegalEntityModify(LegalEntityAddModify):
    
    def fillresponse(self):
        try:
            Responsability.objects.get(individual__user=self.request.user, legal_entity=self.item)
            LegalEntityAddModify.fillresponse(self)
        except:
            raise LucteriosException(IMPORTANT, _("Bad access!"))

@MenuManage.describ(None)
class CurrentLegalEntityShow(LegalEntityShow):
    def fillresponse(self):
        try:
            Responsability.objects.get(individual__user=self.request.user, legal_entity=self.item)
            self.action_list = [('currentmodify', _("Modify"), "images/edit.png", CLOSE_YES)]
            LegalEntityShow.fillresponse(self)
        except:
            raise LucteriosException(IMPORTANT, _("Bad access!"))


@MenuManage.describ(None, FORMTYPE_MODAL, 'core.general', _('View my account.'))
class Account(XferContainerCustom):
    caption = _("My account")
    icon = "account.png"

    def add_legalentity(self, legal_entity):
        self.new_tab(_("Legal entity"))
        self.item = legal_entity
        fields = LegalEntity.get_show_fields()
        self.fill_from_model(1, 1, True, fields[_('001@Identity')])
        self.get_components('name').colspan = 2
        self.get_components('structure_type').colspan = 2
        img_path = get_user_path(
            "contacts", "Image_%s.jpg" % legal_entity.abstractcontact_ptr_id)
        img = XferCompImage('logoimg')
        if exists(img_path):
            img.type = 'jpg'
            img.set_value(readimage_to_base64(img_path))
        else:
            img.set_value(get_icon_path("lucterios.contacts/images/NoImage.png"))
        img.set_location(0, 2, 1, 6)
        self.add_component(img)
        
        btn = XferCompButton('btn_edit')
        btn.set_is_mini(True)
        btn.set_location(4, 1, 1, 2)
        btn.set_action(self.request, CurrentLegalEntityModify.get_action(
            _('Edit'), "images/edit.png"), {'modal': FORMTYPE_MODAL, 'close': CLOSE_NO, 'params': {'legal_entity': legal_entity.id}})
        self.add_component(btn)

    def add_legalentities(self, legal_entities):
        self.new_tab(_("Legal entities"))
        grid = XferCompGrid('legal_entity')
        grid.set_model(legal_entities, LegalEntity.get_default_fields())
        grid.add_action(self.request, CurrentLegalEntityShow.get_action(_("Edit"), "images/show.png"), {'modal': FORMTYPE_MODAL, 'close': CLOSE_NO, 'unique':SELECT_SINGLE})
        grid.set_location(1, 1, 2)
        grid.set_size(200, 500)
        self.add_component(grid)

    def fillresponse(self):
        img = XferCompImage('img')
        img.set_value(get_icon_path('lucterios.contacts/images/account.png'))
        img.set_location(0, 0, 1, 2)
        self.add_component(img)
        lab = XferCompLabelForm("title")
        lab.set_value_as_title(_('View my account.'))
        lab.set_location(1, 0, 2)
        self.add_component(lab)
        try:
            self.item = Individual.objects.get(
                user=self.request.user)
            self.item = self.item.get_final_child()
            self.model = Individual
            self.field_id = 'individual'
            self.params['individual'] = six.text_type(self.item.id)
            self.add_action(AccountAddModify.get_action(
                _("Edit"), "images/edit.png"), {'close': CLOSE_NO})
            is_individual = True
        except ObjectDoesNotExist:
            self.item = LucteriosUser.objects.get(
                id=self.request.user.id)
            self.add_action(UsersEdit.get_action(_("Edit"), "images/edit.png"), {
                            'close': CLOSE_NO, 'params': {'user_actif': six.text_type(self.request.user.id)}})
            is_individual = False
        self.fill_from_model(1, 1, True)
        if is_individual:
            legal_entities = LegalEntity.objects.filter(responsability__individual=self.item).exclude(id=1)
            if len(legal_entities) == 1:
                self.add_legalentity(legal_entities[0])
            elif len(legal_entities) > 1:
                self.add_legalentities(legal_entities)
        self.add_action(WrapAction(_("Close"), "images/close.png"), {})


@MenuManage.describ(None)
class AccountAddModify(XferAddEditor):
    icon = "account.png"
    model = Individual
    field_id = 'individual'
    caption_add = _("My account")
    caption_modify = _("My account")
    locked = True


@MenuManage.describ('', FORMTYPE_MODAL, 'core.general', _('Our structure and its management'))
class CurrentStructure(XferContainerCustom):
    caption = _("Our details")
    icon = "ourDetails.png"
    model = LegalEntity
    field_id = 1

    def fillresponse(self):
        self.params['legal_entity'] = '1'
        img = XferCompImage('img')
        img.set_value(get_icon_path('lucterios.contacts/images/fields.png'))
        img.set_location(0, 0, 1, 2)
        self.add_component(img)
        lab = XferCompLabelForm("title")
        lab.set_value_as_title(_('Our structure and its management'))
        lab.set_location(1, 0, 4)
        self.add_component(lab)
        self.fill_from_model(1, 1, True)
        self.add_action(CurrentStructureAddModify.get_action(
            _("Edit"), "images/edit.png"), {'close': CLOSE_NO})
        self.add_action(CurrentStructurePrint.get_action(
            _("Print"), "images/print.png"), {'close': CLOSE_NO})
        self.add_action(WrapAction(_("Close"), "images/close.png"), {})


@MenuManage.describ('')
class CurrentStructurePrint(XferPrintAction):
    icon = "ourDetails.png"
    model = LegalEntity
    field_id = 1
    caption = _("Our details")
    action_class = CurrentStructure


@MenuManage.describ('CORE.add_parameter')
class CurrentStructureAddModify(XferAddEditor):
    icon = "ourDetails.png"
    model = LegalEntity
    field_id = 1
    caption_add = _("Our details")
    caption_modify = _("Our details")
    locked = True
    redirect_to_show = False

MenuManage.add_sub("contact.conf", "core.extensions", "", _("Contact"), "", 1)


@MenuManage.describ('CORE.change_parameter', FORMTYPE_NOMODAL, 'contact.conf', _('Management functions of individuals and categories of legal entities.'))
class Configuration(XferContainerCustom):
    caption = _("Contacts configuration")
    icon = "contactsConfig.png"

    def _fill_functions(self):
        self.new_tab(_("Functions and responsabilities"))
        img = XferCompImage('imgFunction')
        img.set_value(get_icon_path('lucterios.contacts/images/function.png'))
        img.set_location(0, 0)
        self.add_component(img)
        img = XferCompLabelForm('titleFunction')
        img.set_value_as_title(_("Functions list"))
        img.set_location(1, 0)
        self.add_component(img)
        self.model = Function
        dbfunction = Function.objects.all()
        grid = XferCompGrid("function")
        grid.set_model(dbfunction, None, self)
        grid.add_actions(self)
        grid.set_location(0, 1, 2)
        grid.set_size(200, 500)
        self.add_component(grid)
        lbl = XferCompLabelForm("nbFunction")
        lbl.set_location(0, 2, 2)
        lbl.set_value(_("Number of function show: %d") % grid.nb_lines)
        self.add_component(lbl)

    def _fill_structuretype(self):
        self.new_tab(_("Structure type"))
        img = XferCompImage('imgType')
        img.set_value(get_icon_path('lucterios.contacts/images/category.png'))
        img.set_location(0, 0)
        self.add_component(img)
        img = XferCompLabelForm('titleType')
        img.set_value_as_title(_('Structure types list'))
        img.set_location(1, 0)
        self.add_component(img)
        self.model = StructureType
        dbcategorie = StructureType.objects.all()
        grid = XferCompGrid("structure_type")
        grid.set_model(dbcategorie, None, self)
        grid.add_actions(self)
        grid.set_location(0, 1, 2)
        grid.set_size(200, 500)
        self.add_component(grid)
        lbl = XferCompLabelForm("nbType")
        lbl.set_location(0, 2, 2)
        lbl.set_value(_("Number of structure type show: %d") % grid.nb_lines)
        self.add_component(lbl)

    def _fill_customfield(self):
        self.new_tab(_("Custom field"))
        img = XferCompImage('imgField')
        img.set_value(get_icon_path('lucterios.contacts/images/fields.png'))
        img.set_location(0, 0)
        self.add_component(img)
        img = XferCompLabelForm('titleField')
        img.set_value_as_title(_('custom field list'))
        img.set_location(1, 0)
        self.add_component(img)
        self.model = CustomField
        dbcustom = CustomField.objects.all()
        grid = XferCompGrid("custom_field")
        grid.set_model(dbcustom, None, self)
        grid.add_actions(self)
        grid.set_location(0, 1, 2)
        grid.set_size(200, 500)
        self.add_component(grid)
        lbl = XferCompLabelForm("nbField")
        lbl.set_location(0, 2, 2)
        lbl.set_value(_("Number of custom field show: %d") % grid.nb_lines)
        self.add_component(lbl)

    def fillresponse(self):
        self._fill_functions()
        self._fill_structuretype()
        self._fill_customfield()
        self.add_action(WrapAction(_("Close"), "images/close.png"), {})


@ActionsManage.affect('Function', 'add')
@MenuManage.describ('CORE.add_parameter')
class FunctionAddModify(XferAddEditor):
    icon = "function.png"
    model = Function
    field_id = 'function'
    caption_add = _("Add function")
    caption_modify = _("Modify function")


@ActionsManage.affect('Function', 'delete')
@MenuManage.describ('CORE.add_parameter')
class FunctionDel(XferDelete):
    caption = _("Delete function")
    icon = "function.png"
    model = Function
    field_id = 'function'


@ActionsManage.affect('CustomField', 'add', 'edit')
@MenuManage.describ('CORE.add_parameter')
class CustomFieldAddModify(XferAddEditor):
    icon = "fields.png"
    model = CustomField
    field_id = 'custom_field'
    caption_add = _("Add custom field")
    caption_modify = _("Modify custom field")


@ActionsManage.affect('CustomField', 'delete')
@MenuManage.describ('CORE.add_parameter')
class CustomFieldDel(XferDelete):
    caption = _("Delete custom field")
    icon = "fields.png"
    model = CustomField
    field_id = 'custom_field'


@ActionsManage.affect('StructureType', 'add')
@MenuManage.describ('CORE.add_parameter')
class StructureTypeAddModify(XferAddEditor):
    icon = "function.png"
    model = StructureType
    field_id = 'structure_type'
    caption_add = _("Add structure type")
    caption_modify = _("Modify structure type")


@ActionsManage.affect('StructureType', 'delete')
@MenuManage.describ('CORE.add_parameter')
class StructureTypeDel(XferDelete):
    caption = _("Delete structure type")
    icon = "function.png"
    model = StructureType
    field_id = 'structure_type'


@ActionsManage.affect('PostalCode', 'add')
@MenuManage.describ('contacts.add_postalcode')
class PostalCodeAdd(XferAddEditor):
    caption_add = _("Add function")
    caption_modify = _("Add postal code")
    icon = "postalCode.png"
    model = PostalCode
    field_id = 'postalCode'


@MenuManage.describ('contacts.change_postalcode', FORMTYPE_NOMODAL, 'contact.conf', _('Management of postal codes associated with their communes.'))
class PostalCodeList(XferListEditor):
    caption = _("Postal code")
    icon = "postalCode.png"
    model = PostalCode
    field_id = 'postalCode'

    def fillresponse_header(self):
        filter_postal_code = self.getparam('filter_postal_code')
        if filter_postal_code is None:
            local_struct = LegalEntity.objects.get(
                id=1)
            filter_postal_code = six.text_type(local_struct.postal_code)
        lbl = XferCompLabelForm('filtre')
        lbl.set_value_as_name(_('Filtrer by postal code'))
        lbl.set_location(1, 0)
        self.add_component(lbl)
        comp = XferCompEdit('filter_postal_code')
        comp.set_value(filter_postal_code)
        comp.set_action(self.request, self.get_action(),
                        {'modal': FORMTYPE_REFRESH, 'close': CLOSE_NO})
        comp.set_location(1, 1)
        self.add_component(comp)
        self.filter = Q(postal_code__startswith=filter_postal_code)


@MenuManage.describ('contacts.change_postalcode', FORMTYPE_MODAL, 'contact.conf', _('Tool to import contacts from CSV file.'))
class ContactImport(XferContainerCustom):
    caption = _("Contact import")
    icon = "contactsConfig.png"

    def __init__(self, **kwargs):
        XferContainerCustom.__init__(self, **kwargs)
        self.model = None
        self.quotechar = ""
        self.delimiter = ""
        self.encoding = ""
        self.dateformat = ""
        self.spamreader = None

    def _select_csv_parameters(self):
        lbl = XferCompLabelForm('lbl_modelname')
        lbl.set_value_as_name(_('model'))
        lbl.set_location(1, 0)
        self.add_component(lbl)
        model_select = XferCompSelect('modelname')
        if self.model is not None:
            model_select.set_value(self.model.get_long_name())
        model_select.set_select(AbstractContact.get_select_contact_type(False))
        model_select.set_location(2, 0, 3)
        self.add_component(model_select)
        lbl = XferCompLabelForm('lbl_csvcontent')
        lbl.set_value_as_name(_('CSV file'))
        lbl.set_location(1, 1)
        self.add_component(lbl)
        upld = XferCompUpLoad('csvcontent')
        upld.http_file = True
        upld.add_filter(".csv")
        upld.set_location(2, 1, 3)
        self.add_component(upld)
        lbl = XferCompLabelForm('lbl_encoding')
        lbl.set_value_as_name(_('encoding'))
        lbl.set_location(1, 2)
        self.add_component(lbl)
        lbl = XferCompEdit('encoding')
        lbl.set_value(self.encoding)
        lbl.set_location(2, 2)
        self.add_component(lbl)
        lbl = XferCompLabelForm('lbl_dateformat')
        lbl.set_value_as_name(_('date format'))
        lbl.set_location(3, 2)
        self.add_component(lbl)
        lbl = XferCompEdit('dateformat')
        lbl.set_value(self.dateformat)
        lbl.set_location(4, 2)
        self.add_component(lbl)
        lbl = XferCompLabelForm('lbl_delimiter')
        lbl.set_value_as_name(_('delimiter'))
        lbl.set_location(1, 3)
        self.add_component(lbl)
        lbl = XferCompEdit('delimiter')
        lbl.set_value(self.delimiter)
        lbl.set_location(2, 3)
        self.add_component(lbl)
        lbl = XferCompLabelForm('lbl_quotechar')
        lbl.set_value_as_name(_('quotechar'))
        lbl.set_location(3, 3)
        self.add_component(lbl)
        lbl = XferCompEdit('quotechar')
        lbl.set_value(self.quotechar)
        lbl.set_location(4, 3)
        self.add_component(lbl)
        return lbl

    def _read_csv(self):
        if self.quotechar == '':
            current_quoting = QUOTE_NONE
        else:
            current_quoting = QUOTE_ALL
        if 'csvcontent' in self.request.FILES.keys():
            csvfile = TextIOWrapper(
                self.request.FILES['csvcontent'].file, encoding=self.encoding, errors='replace')
            csvcontent = "".join(csvfile.readlines())
            for param_idx in range(0, int(len(csvcontent) / 2048) + 2):
                self.params['csvcontent%d' % param_idx] = csvcontent[
                    2048 * param_idx:2048 * (param_idx + 1)]
            csvfile.seek(0)
        else:
            csvcontent = ""
            for param_idx in range(0, 1000):
                curent_content = self.getparam('csvcontent%d' % param_idx)
                if curent_content is None:
                    break
                else:
                    csvcontent += "" + curent_content
            csvfile = StringIO(csvcontent)
        self.spamreader = DictReader(
            csvfile, delimiter=self.delimiter, quotechar=self.quotechar, quoting=current_quoting)
        if (self.spamreader.fieldnames is None) or (len(self.spamreader.fieldnames) == 0):
            raise LucteriosException(IMPORTANT, _('CSV file unvalid!'))

    def _select_fields(self):
        select_list = [('', None)]
        for fieldname in self.spamreader.fieldnames:
            select_list.append((fieldname, fieldname))
        row = 0
        for fieldname in self.model.get_import_fields():
            if isinstance(fieldname, tuple):
                fieldname, title = fieldname
                is_need = False
            else:
                dep_field = self.model.get_field_by_name(fieldname)
                title = dep_field.verbose_name
                is_need = not dep_field.blank and not dep_field.null
            lbl = XferCompLabelForm('lbl_' + fieldname)
            lbl.set_value_as_name(title)
            lbl.set_location(1, row)
            self.add_component(lbl)
            lbl = XferCompSelect('fld_' + fieldname)
            lbl.set_select(deepcopy(select_list))
            lbl.set_value("")
            lbl.set_needed(is_need)
            lbl.set_location(2, row)
            self.add_component(lbl)
            row += 1

    def _show_initial_csv(self):
        tbl = XferCompGrid('CSV')
        for fieldname in self.spamreader.fieldnames:
            tbl.add_header(fieldname, fieldname)
        row_idx = 1
        for row in self.spamreader:
            if row[self.spamreader.fieldnames[-1]] is not None:
                for fieldname in self.spamreader.fieldnames:
                    tbl.set_value(row_idx, fieldname, row[fieldname])
                row_idx += 1
        tbl.set_location(1, 1, 2)
        self.add_component(tbl)
        lbl = XferCompLabelForm('nb_line')
        lbl.set_value(_("Total number of contacts: %d") % (row_idx - 1))
        lbl.set_location(1, 2, 2)
        self.add_component(lbl)

    def _read_csv_and_convert(self):
        fields_association = {}
        for param_key in self.params.keys():
            if (param_key[:4] == 'fld_') and (self.params[param_key] != ""):
                fields_association[param_key[4:]] = self.params[param_key]
        fields_description = []
        for fieldname in self.model.get_import_fields():
            if isinstance(fieldname, tuple):
                fieldname, title = fieldname
            else:
                dep_field = self.model.get_field_by_name(fieldname)
                title = dep_field.verbose_name
                is_date = isinstance(dep_field, DateField)
            if fieldname in fields_association.keys():
                fields_description.append(
                    (fieldname, title, is_date))
        self._read_csv()
        csv_readed = []
        for row in self.spamreader:
            if row[self.spamreader.fieldnames[-1]] is not None:
                new_row = {}
                for field_description in fields_description:
                    if field_description[2]:
                        try:
                            new_row[field_description[0]] = datetime.strptime(
                                row[fields_association[field_description[0]]], self.dateformat).date()
                        except (TypeError, ValueError):
                            new_row[field_description[0]] = datetime.today()
                    else:
                        new_row[field_description[0]] = row[
                            fields_association[field_description[0]]]
                csv_readed.append(new_row)
        return fields_description, csv_readed

    def fillresponse(self, modelname, quotechar="'", delimiter=",", encoding="utf-8", dateformat="%d/%m/%Y", step=0):
        if modelname is not None:
            self.model = apps.get_model(modelname)
        if six.PY2:
            self.quotechar = six.binary_type(quotechar)
            self.delimiter = six.binary_type(delimiter)
        else:
            self.quotechar = quotechar
            self.delimiter = delimiter
        self.encoding = encoding
        self.dateformat = dateformat

        img = XferCompImage('img')
        img.set_value(self.icon_path())
        img.set_location(0, 0, 1, 6)
        self.add_component(img)
        if step == 0:
            lbl = self._select_csv_parameters()
            step = 1
        elif step == 1:
            lbl = XferCompLabelForm('lbl_modelname')
            lbl.set_value_as_name(_('model'))
            lbl.set_location(1, 0)
            self.add_component(lbl)
            lbl = XferCompLabelForm('modelname')
            lbl.set_value(self.model._meta.verbose_name.title())
            lbl.set_location(2, 0)
            self.add_component(lbl)
            self._read_csv()
            self.new_tab(_("Fields"))
            self._select_fields()
            self.new_tab(_("Current content"))
            self._show_initial_csv()
            step = 2
        elif step == 2:
            lbl = XferCompLabelForm('lbl_modelname')
            lbl.set_value_as_name(_('model'))
            lbl.set_location(1, 0)
            self.add_component(lbl)
            lbl = XferCompLabelForm('modelname')
            lbl.set_value(self.model._meta.verbose_name.title())
            lbl.set_location(2, 0)
            self.add_component(lbl)
            fields_description, csv_readed = self._read_csv_and_convert()
            tbl = XferCompGrid('CSV')
            for field_description in fields_description:
                tbl.add_header(field_description[0], field_description[1])
            row_idx = 1
            for row in csv_readed:
                for field_description in fields_description:
                    tbl.set_value(
                        row_idx, field_description[0], row[field_description[0]])
                row_idx += 1
            tbl.set_location(1, 1, 2)
            self.add_component(tbl)
            lbl = XferCompLabelForm('nb_line')
            lbl.set_value(_("Total number of contacts: %d") % (row_idx - 1))
            lbl.set_location(1, 2, 2)
            self.add_component(lbl)
            step = 3
        elif step == 3:
            fields_description, csv_readed = self._read_csv_and_convert()
            items_imported = {}
            for rowdata in csv_readed:
                new_item = self.model.import_data(rowdata, dateformat)
                if new_item is not None:
                    items_imported[new_item.id] = new_item
            lbl = XferCompLabelForm('result')
            lbl.set_value_as_header(
                _("%d contacts are been imported") % len(items_imported))
            lbl.set_location(1, 2, 2)
            self.add_component(lbl)
            step = 4
        if step < 4:
            if step > 1:
                self.add_action(self.get_action(_('Back'), "images/left.png"),
                                {'close': CLOSE_NO, 'modal': FORMTYPE_REFRESH, 'params': {'step': step - 2}})
            self.add_action(self.get_action(_('Ok'), "images/ok.png"),
                            {'close': CLOSE_NO, 'modal': FORMTYPE_REFRESH, 'params': {'step': step}})
            self.add_action(WrapAction(_("Cancel"), "images/cancel.png"), {})
        else:
            self.add_action(WrapAction(_("Close"), "images/close.png"), {})


@signal_and_lock.Signal.decorate('config')
def config_contacts(xfer):
    Params.fill(xfer, ['contacts-mailtoconfig'], 1, 10)
    xfer.params['params'].append('contacts-mailtoconfig')
    return True
