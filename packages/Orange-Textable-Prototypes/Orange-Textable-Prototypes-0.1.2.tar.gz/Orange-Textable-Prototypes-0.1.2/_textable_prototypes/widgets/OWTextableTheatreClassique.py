"""
<name>Theatre Classique</name>
<description>Import XML-TEI data from theatre-classique website</description>
<icon>icons/Theatre_Classique.png</icon>
<priority>10</priority>
"""

__version__ = u'0.1.0'

import Orange
from OWWidget import *
import OWGUI

from _textable.widgets.LTTL.Segmentation import Segmentation
from _textable.widgets.LTTL.Input import Input
from _textable.widgets.LTTL.Segmenter import Segmenter
from _textable.widgets.LTTL.Processor import Processor
from _textable.widgets.LTTL.Recoder import Recoder

from _textable.widgets.TextableUtils import *   # Provides several utilities.

import urllib2
import re
import inspect
import os
import pickle


class OWTextableTheatreClassique(OWWidget):
    """Orange widget for importing XML-TEI data from the Theatre-classique
    website (http://www.theatre-classique.fr)
    """

    # Widget settings declaration...
    settingsList = [
        u'autoSend',
        u'label',
        u'uuid',
        u'selectedTitles',
        u'filterCriterion',
        u'filterValue',
        u'importedURLs',
        u'displayAdvancedSettings',
    ]

    def __init__(self, parent=None, signalManager=None):
        """Widget creator."""

        # Standard call to creator of base class (OWWidget).
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0)

        # Channel definitions...
        self.inputs = []
        self.outputs = [('Text data', Segmentation)]

        # Settings initializations...
        self.autoSend = True
        self.label = u'xml_tei_data'
        self.filterCriterion = u'author'
        self.filterValue = u'(all)'
        self.titleLabels = list()
        self.selectedTitles = list()
        self.importedURLs = list()
        self.displayAdvancedSettings = False

        # Always end Textable widget settings with the following 3 lines...
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)

        # Other attributes...
        self.segmenter = Segmenter()
        self.processor = Processor()
        self.segmentation = None
        self.createdInputs = list()
        self.titleSeg = None
        self.filteredTitleSeg = None
        self.filterValues = dict()
        self.base_url =     \
          u'http://www.theatre-classique.fr/pages/programmes/PageEdition.php'
        self.document_base_url =     \
          u'http://www.theatre-classique.fr/pages/'

        # Next two instructions are helpers from TextableUtils. Corresponding
        # interface elements are declared here and actually drawn below (at
        # their position in the UI)...
        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(
            widget=self.controlArea,
            master=self,
            callback=self.sendData,
            infoBoxAttribute=u'infoBox',
            sendIfPreCallback=self.updateGUI,
        )

        # The AdvancedSettings class, also from TextableUtils, facilitates
        # the management of basic vs. advanced interface. An object from this 
        # class (here assigned to self.advancedSettings) contains two lists 
        # (basicWidgets and advanceWidgets), to which the corresponding
        # widgetBoxes must be added.
        self.advancedSettings = AdvancedSettings(
            widget=self.controlArea,
            master=self,
            callback=self.updateFilterValueList,
        )

        # User interface...

        # Advanced settings checkbox (basic/advanced interface will appear 
        # immediately after it...
        self.advancedSettings.draw()

        # Filter box (advanced settings only)
        filterBox = OWGUI.widgetBox(
            widget=self.controlArea,
            box=u'Filter',
            orientation=u'vertical',
        )
        filterCriterionCombo = OWGUI.comboBox(
            widget=filterBox,
            master=self,
            value=u'filterCriterion',
            items=[u'author', u'year', u'genre'],
            sendSelectedValue=True,
            orientation=u'horizontal',
            label=u'Criterion:',
            labelWidth=180,
            callback=self.updateFilterValueList,
            tooltip=(
                u"Tool\n"
                u"tips."
            ),
        )
        filterCriterionCombo.setMinimumWidth(120)
        OWGUI.separator(widget=filterBox, height=3)
        self.filterValueCombo = OWGUI.comboBox(
            widget=filterBox,
            master=self,
            value=u'filterValue',
            sendSelectedValue=True,
            orientation=u'horizontal',
            label=u'Value:',
            labelWidth=180,
            callback=self.updateTitleList,
            tooltip=(
                u"Tool\n"
                u"tips."
            ),
        )
        OWGUI.separator(widget=filterBox, height=3)
        
        # The following lines add filterBox (and a vertical separator) to the
        # advanced interface...
        self.advancedSettings.advancedWidgets.append(filterBox)
        self.advancedSettings.advancedWidgetsAppendSeparator()

        # Title box
        titleBox = OWGUI.widgetBox(
            widget=self.controlArea,
            box=u'Titles',
            orientation=u'vertical',
        )
        self.titleListbox = OWGUI.listBox(
            widget=titleBox,
            master=self,
            value=u'selectedTitles',    # setting (list)
            labels=u'titleLabels',      # setting (list)
            callback=self.sendButton.settingsChanged,
            tooltip=u"The list of titles whose content will be imported",
        )
        self.titleListbox.setMinimumHeight(150)
        self.titleListbox.setSelectionMode(3)
        OWGUI.separator(widget=titleBox, height=3)
        OWGUI.button(
            widget=titleBox,
            master=self,
            label=u'Refresh',
            callback=self.refreshTitleSeg,
            tooltip=u"Connect to Theatre-classique website and refresh list.",
        )
        OWGUI.separator(widget=titleBox, height=3)

        OWGUI.separator(widget=self.controlArea, height=3)

        # From TextableUtils: a minimal Options box (only segmentation label).
        basicOptionsBox = BasicOptionsBox(self.controlArea, self)
 
        OWGUI.separator(widget=self.controlArea, height=3)

        # Now Info box and Send button must be drawn...
        self.infoBox.draw()
        self.sendButton.draw()
        
        # This initialization step needs to be done after infoBox has been 
        # drawn (because getTitleSeg may need to display an error message).
        self.getTitleSeg()

        # Send data if autoSend.
        self.sendButton.sendIf()

    def sendData(self):
        """Compute result of widget processing and send to output"""

        # Skip if title list is empty:
        if self.titleLabels == list():
            return
        
        # Check that something has been selected...
        if len(self.selectedTitles) == 0:
            self.infoBox.noDataSent(u': no title selected.')
            self.send(u'Text data', None, self)
            return

        # Check that label is not empty...
        if not self.label:
            self.infoBox.noDataSent(warning=u'No label was provided.')
            self.send(u'Text data', None, self)
            return

        # Clear created Inputs.
        self.clearCreatedInputs()
        
        # Initialize progress bar.
        progressBar = OWGUI.ProgressBar(
            self, 
            iterations=len(self.selectedTitles)
        )       
        
        # Attempt to connect to Theatre-classique and retrieve plays...
        xml_contents = list()
        annotations = list()
        try:
            for title in self.selectedTitles:
                response = urllib2.urlopen(
                    self.document_base_url + 
                    self.filteredTitleSeg[title].annotations[u'url']
                )
                xml_contents.append(unicode(response.read(), u'utf8'))
                annotations.append(
                    self.filteredTitleSeg[title].annotations.copy()
                )
                progressBar.advance()   # 1 tick on the progress bar...

        # If an error occurs (e.g. http error, or memory error)...
        except:

            # Set Info box and widget to 'error' state.
            self.infoBox.noDataSent(
                error=u"Couldn't download data from theatre-classique website."
            )

            # Reset output channel.
            self.send(u'Text data', None, self)
            return
            
        # Store downloaded XML in input objects and annotate them...
        for xml_content_idx in xrange(len(xml_contents)):
            newInput = Input(xml_contents[xml_content_idx], self.label)
            newInput[0].annotations = annotations[xml_content_idx]
            self.createdInputs.append(newInput)
            
        # If there's only one play, the widget's output is the created Input.
        if len(self.createdInputs) == 1:
            self.segmentation = self.createdInputs[0]
            
        # Otherwise the widget's output is a concatenation...
        else:
            self.segmentation = self.segmenter.concatenate(
                self.createdInputs,
                self.label,
                import_labels_as=None,
            )

        # Store imported URLs as setting.
        self.importedURLs = [
            self.filteredTitleSeg[self.selectedTitles[0]].annotations[u'url']
        ]
        
        # Set status to OK and report data size...
        message = u'%i segment@p ' % len(self.segmentation)
        message = pluralize(message, len(self.segmentation))
        numChars = 0
        for segment in self.segmentation:
            segmentLength = len(Segmentation.data[segment.address.str_index])
            numChars += segmentLength
        message += u'(%i character@p).' % numChars
        message = pluralize(message, numChars)
        self.infoBox.dataSent(message)

        # Clear progress bar.
        progressBar.finish()
        
        # Send token...
        self.send(u'Text data', self.segmentation, self)
        self.sendButton.resetSettingsChangedFlag()        
        
    def getTitleSeg(self):
        """Get title segmentation, either saved locally or online"""
        
        # Try to open saved file in this module's directory...
        path = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe()))
        )
        try:
            file = open(os.path.join(path, "cached_title_list"),'r')
            self.titleSeg = pickle.load(file)
            file.close()
        # Else try to load list from Theatre-classique and build new seg...
        except IOError:
            self.titleSeg = self.getTitleListFromTheatreClassique()

        # Build author, year and genre lists...
        if self.titleSeg is not None:
            self.filterValues[u'author'] = self.processor.count_in_context(
                units={
                    u'segmentation': self.titleSeg, 
                    u'annotation_key': u'author'
                }
            ).col_ids
            self.filterValues[u'author'].sort()
            self.filterValues[u'year'] = self.processor.count_in_context(
                units={
                    u'segmentation': self.titleSeg, 
                    u'annotation_key': u'year'
                }
            ).col_ids
            self.filterValues[u'year'].sort(key=lambda v: int(v))
            self.filterValues[u'genre'] = self.processor.count_in_context(
                units={
                    u'segmentation': self.titleSeg, 
                    u'annotation_key': u'genre'
                }
            ).col_ids
            self.filterValues[u'genre'].sort()

        # Update title and filter value lists (only at init and on manual
        # refresh, therefore separate from self.updateGUI).
        self.updateFilterValueList()
                    
    def refreshTitleSeg(self):
        """Refresh title segmentation from website"""
        self.titleSeg = self.getTitleListFromTheatreClassique()
        # Update title and filter value lists (only at init and on manual
        # refresh, therefore separate from self.updateGUI).
        self.updateFilterValueList()
        
    def getTitleListFromTheatreClassique(self):
        """Fetch titles from the Theatre-classique website"""

        self.infoBox.customMessage(
            u'Fetching data from Theatre-classique website, please wait'
        )
        
        # Attempt to connect to Theatre-classique...
        try:
            response = urllib2.urlopen(self.base_url)
            base_html = unicode(response.read(), 'iso-8859-1')
            self.infoBox.customMessage(
                u'Done fetching data from Theatre-classique website.'
            )

        # If unable to connect (somehow)...
        except:

            # Set Info box and widget to 'warning' state.
            self.infoBox.noDataSent(
                warning=u"Couldn't access theatre-classique website."
            )

            # Empty title list box.
            self.titleLabels = list()

            # Reset output channel.
            self.send(u'Text data', None, self)
            return None
            
        # Otherwise store HTML content in LTTL Input object.
        base_html_seg = Input(base_html)

        # Remove accents from the data...
        recoder = Recoder(remove_accents=True)
        recoded_seg = recoder.apply(base_html_seg, mode=u"standard")

        # Extract table containing titles from HTML.
        table_seg = self.segmenter.import_xml(
            segmentation=recoded_seg,
            element=u'table',
            conditions={u'id': re.compile(ur'^table_AA$')},
            remove_markup=False,
        )

        # Extract table lines.
        line_seg = self.segmenter.import_xml(
            segmentation=table_seg,
            element=u'tr',
            remove_markup=False,
        )

        # Compile the regex that will be used to parse each line.
        field_regex = re.compile(
            ur"^\s*<td>\s*<a.+?>(.+?)</a>\s*</td>\s*"
            ur"<td>(.+?)</td>\s*"
            ur"<td.+?>\s*<a.+?>\s*(\d+?)\s*</a>\s*</td>\s*"
            ur"<td.+?>\s*(.+?)\s*</td>\s*"
            ur"<td.+?>\s*<a\s+.+?t=\.{2}/(.+?)'>\s*HTML"
        )

        # Parse each line and store the resulting segmentation in an attribute.
        titleSeg = self.segmenter.tokenize(
            segmentation=line_seg,
            regexes=[
                (field_regex, u'Tokenize', {u'author': u'&1'}),
                (field_regex, u'Tokenize', {u'title': u'&2'}),
                (field_regex, u'Tokenize', {u'year': u'&3'}),
                (field_regex, u'Tokenize', {u'genre': u'&4'}),
                (field_regex, u'Tokenize', {u'url': u'&5'}),
            ],
            import_annotations=False,
        )

        # Sort this segmentation alphabetically based on titles...
        titleSeg.segments.sort(key=lambda s: s.annotations[u'title'])
        
        # Try to save list in this module's directory for future reference...
        path = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe()))
        )
        try:
            file = open(os.path.join(path, u"cached_title_list"), u'wb')
            pickle.dump(titleSeg, file) 
            file.close()         
        except IOError:
            pass

        # Remove warning (if any)...
        self.error(0)
        self.warning(0)
        
        return titleSeg

    def updateFilterValueList(self):
        """Update the list of filter values"""
        
        # In Advanced settings mode, populate filter value list...
        if self.titleSeg is not None and self.displayAdvancedSettings:
            self.filterValueCombo.clear()
            self.filterValueCombo.addItem(u'(all)')
            for filterValue in self.filterValues[self.filterCriterion]:
                self.filterValueCombo.addItem(filterValue)

        # Reset filterValue if needed...
        if self.filterValue not in [
            unicode(self.filterValueCombo.itemText(i)) 
            for i in xrange(self.filterValueCombo.count())
        ]:
            self.filterValue = u'(all)'
        else:
            self.filterValue = self.filterValue
        
        self.updateTitleList()

    def updateTitleList(self):
        """Update the list of titles"""
        
        # If titleSeg has not been loaded for some reason, skip.
        if self.titleSeg is None:
            return
        
        # In Advanced settings mode, get list of selected titles...
        if self.displayAdvancedSettings and self.filterValue != u'(all)':
            self.filteredTitleSeg, _ = self.segmenter.select(
                segmentation=self.titleSeg,
                regex=re.compile(ur'^%s$' % self.filterValue),
                annotation_key=self.filterCriterion,
            )
        else:
            self.filteredTitleSeg = self.titleSeg
        
        # Populate titleLabels list with the titles...
        self.titleLabels = sorted(
            [s.annotations[u'title'] for s in self.filteredTitleSeg]
        )
        
        # Add specification (author, year and genre, depending on criterion)...
        titleLabels = self.titleLabels[:]
        for idx in xrange(len(titleLabels)):
            titleLabel = titleLabels[idx]
            specs = list()
            if (
                self.displayAdvancedSettings == False or
                self.filterCriterion != 'author' or 
                self.filterValue == u'(all)'
            ):
                specs.append(
                    self.filteredTitleSeg[idx].annotations[u'author']
                )
            if (
                self.displayAdvancedSettings == False or
                self.filterCriterion != 'year' or 
                self.filterValue == u'(all)'
            ):
                specs.append(
                    self.filteredTitleSeg[idx].annotations[u'year']
                )
            if (
                self.displayAdvancedSettings == False or
                self.filterCriterion != 'genre' or 
                self.filterValue == u'(all)'
            ):
                specs.append(
                    self.filteredTitleSeg[idx].annotations[u'genre']
                )
            titleLabels[idx] = titleLabel + " (%s)" % "; ".join(specs)
        self.titleLabels = titleLabels
        
        # Reset selectedTitles if needed...
        if not set(self.importedURLs).issubset(
            set(u.annotations[u'url'] for u in self.filteredTitleSeg)
        ):
            self.selectedTitles = list()
        else:
            self.selectedTitles = self.selectedTitles

        self.sendButton.settingsChanged()

    def updateGUI(self):
        """Update GUI state"""
        if self.displayAdvancedSettings:
            self.advancedSettings.setVisible(True)
        else:
            self.advancedSettings.setVisible(False)
            
        if len(self.titleLabels) > 0:
            self.selectedTitles = self.selectedTitles
            
    def clearCreatedInputs(self):
        """Delete all Input objects that have been created."""
        # Delete strings...
        for i in self.createdInputs:
            i.clear()
        # Empty list of created inputs.
        del self.createdInputs[:]
        # Delete those created inputs that are at the end of the string store.
        for i in reversed(xrange(len(Segmentation.data))):
            if Segmentation.data[i] is None:
                Segmentation.data.pop(i)
            else:
                break

    def onDeleteWidget(self):
        """Free memory when widget is deleted (overriden method)"""
        self.clearCreatedInputs()

    # The following two methods need to be copied (without any change) in
    # every Textable widget...

    def getSettings(self, *args, **kwargs):
        """Read settings, taking into account version number (overriden)"""
        settings = OWWidget.getSettings(self, *args, **kwargs)
        settings["settingsDataVersion"] = __version__.split('.')[:2]
        return settings

    def setSettings(self, settings):
        """Write settings, taking into account version number (overriden)"""
        if settings.get("settingsDataVersion", None) \
                == __version__.split('.')[:2]:
            settings = settings.copy()
            del settings["settingsDataVersion"]
            OWWidget.setSettings(self, settings)


if __name__ == '__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWTextableTheatreClassique()
    myWidget.show()
    myApplication.exec_()
