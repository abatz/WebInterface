<?php
foreach($_POST as $k=>$v){
        ${$k} = $v;  // variable variable (adjective noun)
}

$error = "";
$data = array();

$filename = urlencode("colorbar_{$variable}.png");
$data['colorbar'] = "images/{$filename}";

$data['error']=$error;
$data['status'] = ($error) ? 'failure' : 'success';
header("content-type = application/json");
echo json_encode($data);
exit();
?>
