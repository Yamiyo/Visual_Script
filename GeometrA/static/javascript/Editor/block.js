Blockly.Blocks['main'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Main");
    this.setInputsInline(true);
    this.setNextStatement(true, null);
    this.setColour(197);
 this.setTooltip("This is the start of workspace. ");
 this.setHelpUrl("");
  }
};

Blockly.Python['main'] = function(block) {
    var code = "Main\\";
    return code;
}

Blockly.Blocks['sleep'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Sleep(s)")
        .appendField(new Blockly.FieldNumber(0, 0, 60), "Time");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(225);
 this.setTooltip("This is an action for you to wait for few seconds. (Domain is between 0 and 60.)");
 this.setHelpUrl("");
  }
};

Blockly.Python['sleep'] = function(block) {
    var code = "Sleep(s)|" + block.getFieldValue("Time") + '\\';
    return code;
}

Blockly.Blocks['swipe'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Swipe")
        .appendField("start: ")
        .appendField("x")
        .appendField(new Blockly.FieldTextInput("0"), "startX")
        .appendField("y")
        .appendField(new Blockly.FieldTextInput("0"), "startY")
        .appendField(", end: ")
        .appendField("x")
        .appendField(new Blockly.FieldTextInput("0"), "EndX")
        .appendField("y")
        .appendField(new Blockly.FieldTextInput("0"), "EndY");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("This is an action for you to swipe on the device!");
 this.setHelpUrl("");
  }
};

Blockly.Python['swipe'] = function(block) {
  var text_startx = block.getFieldValue('startX');
  var text_starty = block.getFieldValue('startY');
  var text_endx = block.getFieldValue('EndX');
  var text_endy = block.getFieldValue('EndY');
  var code = "Swipe|start x=" + text_startx + ", y=" + text_starty + ", end x=" + text_endx + ", y=" + text_endy + "\\";
  return code;
};

Blockly.Blocks['set_text'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Set Text ")
        .appendField(new Blockly.FieldTextInput(""), "content");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("This is an action for you to input the text on device!");
 this.setHelpUrl("");
  }
};

Blockly.Python['set_text'] = function(block) {
  var text_content = block.getFieldValue('content');
  var code = 'Set Text|' + text_content + '\\';
  return code;
};

Blockly.Blocks['android_keycode'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Android Keycode ")
        .appendField(new Blockly.FieldTextInput(""), "keycode");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("This is an action for you to use the key codes provided by Android; you can use it with either key code name or key code index. ");
 this.setHelpUrl("https://github.com/NTUTVisualScript/GeometrA/blob/master/docs/KeycodeList.md");
  }
};

Blockly.Python['android_keycode'] = function(block) {
  var text_keycode = block.getFieldValue('keycode');
  var code = 'Android Keycode|' + text_keycode + "\\";
  return code;
};

Blockly.Blocks['loop'] = {
  init: function() {
    this.appendStatementInput("Loop")
        .setCheck(null)
        .appendField("Loop")
        .appendField(new Blockly.FieldNumber(1, 1), "times");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(160);
 this.setTooltip("This is an action for you to execute your code iteratively.");
 this.setHelpUrl("");
  }
};

Blockly.Python['loop'] = function(block) {
  var number_times = block.getFieldValue('times');
  var statements_loop = Blockly.Python.statementToCode(block, 'Loop');
  var code = '...\n';
  return code;
};


Blockly.Blocks['click'] = {
  init: function() {
    this.appendDummyInput("clickInput")
        .appendField("Click")
        .appendField(new Blockly.FieldImage("https://neil.fraser.name/common/yes.gif", 100, 100, "*"), "image");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(220);
    this.getField('image').EDITABLE = true;
    this.setTooltip("This is an action for you to click on your device.");
    this.setHelpUrl("");
  },
  update: function(data){
        this.getField("image").setValue(data);
  }
};

Blockly.Python['click'] = function(block) {
    var image = block.getFieldValue('image');
    var code = 'Click|' + image + '\\';
    return code;
};
