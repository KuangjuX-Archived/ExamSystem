home.php
<!DOCTYPE html>
<html>
    <head>
        <title>Home</title>
        <meta charset="UTF-8">
    </head>
    <body>
    <p><strong>Welcome to our website!</strong></p>
    <?php
        require_once "exam.php";


        $obj = new exam("root","","localhost","exam");
        //print_r($obj);
        //print_r($_SESSION["row"]);
        //$obj->connect();
        if($_POST["answer"]!="Enter")
        {
            $answer=$_POST["answer"];
            $obj->judge($answer);

        }
        else
        {
            $row=$obj->select();
            $_SESSION["answer"]=$_SESSION["row"]["question_answer"];

        }
    ?>
    <p>Click here to return to answer the question.<br/></p>
    <a href="index.html">Return</a>
    </body>
</html>
