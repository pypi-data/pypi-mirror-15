cw.cubes.datacat = {
    // Initialize dependent form select fields and bind update event on
    // change on the master select.
    initDependentFormField: function(masterSelectId,
                                     dependentSelectInfo) {
        var masterSelect = cw.jqNode(masterSelectId);
        // XXX no sure .change is the best event here...
        masterSelect.change(function(){
            cw.cubes.datacat.updateDependentFormField(this, dependentSelectInfo);
        });
    },

    // Update dependent form select fields.
    updateDependentFormField: function(masterSelect,
                                       dependentSelectInfo) {
        let dependentSelectId;
        let groupId;
        let octetStreamId;
        for (let etype in dependentSelectInfo) {
            dependentSelectId = dependentSelectInfo[etype];
            // Clear previously selected value.
            var dependentSelect = cw.jqNode(dependentSelectId);
            $(dependentSelect).val('');
            // Hide all optgroups.
            $(dependentSelect).find('optgroup').hide();
            // But the one corresponding to the master select.
            groupId = '#' + etype.toLowerCase() + '_mediatype_' + $(masterSelect).val().replace('/', '-');
            $(groupId).show();
            // Always show application/octet-stream choices.
            octetStreamId = '#' + etype.toLowerCase() + '_mediatype_application-octet-stream';
            $(octetStreamId).show();
        }
    }
}
