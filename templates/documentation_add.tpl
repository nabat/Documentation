<form action='$SELF_URL' METHOD='post' name='FORM_DOC' ID='FORM_DOC' class='form-horizontal' role='form'>
  <input type=hidden name='index' value='$index'>
  <fieldset>
    <div class='box box-theme box-form'>
      <div class='box-header with-border'><h4 class='box-title'>%TITLE%</h4></div>
      <div class='box-body'>

        <div class='form-group'>
          <label for='WIKI' class='control-label col-md-4 col-sm-2  required'>Wiki URL:</label>

          <div class='col-md-8 col-sm-8'>
            <input type=text class='form-control' required id='WIKI' name='WIKI' value='%WIKI%'>
          </div>
        </div>
        <div class='form-group'>
          <label for='CONFLUENCE' class='control-label col-md-4 col-sm-2 required'>Confluence URL:</label>

          <div class='col-md-8 col-sm-8'>
            <input type='text' class='form-control' id='CONFLUENCE' name='CONFLUENCE' value='%CONFLUENCE%' required >
          </div>
        </div>

        <div class='box-footer'>
         %SUBMIT%
        </div>
      </div>

    </div>

  </fieldset>
</form>
