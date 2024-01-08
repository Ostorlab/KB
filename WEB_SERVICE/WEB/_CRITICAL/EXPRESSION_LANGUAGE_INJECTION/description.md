Expression Language Injection (EL Injection) is a critical vulnerability arising from the mishandling of user inputs within expression languages commonly utilized in web applications. These languages serve to dynamically access and modify data. Attackers exploit EL Injection by surreptitiously injecting malevolent code into these expressions. This unauthorized tampering can result in severe consequences, including unauthorized access, data breaches, or even the execution of remote code.

EL Injection primarily manifests within frameworks or templates supporting expression languages like JSP (JavaServer Pages), JSF (JavaServer Faces), Apache Struts, Thymeleaf, and various others commonly employed in web application development.

### Example


=== Java
  ```java
  @RequestMapping(value="/")
    String index() {
    if ( hasErrors() ) {
        return "redirect:/error?msg=error.generic";
    } else {
        return "index";`
    }
    }
  ```
=== JSP
  ```jsp
    <spring:message code="${param.msg}" />
  ```
