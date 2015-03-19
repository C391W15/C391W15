<HTML>
<HEAD>
<TITLE>Personal Info</TITLE>
</HEAD>

<BODY>

<%@ page import="java.sql.*"%>
<%@ page import="java.util.*"%>

<%
	Connection conn = null;
    String driverName = (String) session.getAttribute("driverName");
    String dbstring = (String) session.getAttribute("dbstring");
    String userName = (String) session.getAttribute("userName");
    int person_id = (Integer) session.getAttribute("person_id");


    try{
        //load and register the driver
        Class drvClass = Class.forName(driverName); 
        DriverManager.registerDriver((Driver) drvClass.newInstance());
    } catch(Exception ex){
        out.println("<hr>" + ex.getMessage() + "<hr>");
    }

    try{
        //establish the connection 
        conn = DriverManager.getConnection(dbstring,"cdingram","Oracle_88");
        conn.setAutoCommit(false);
    } catch(Exception ex){
    
        out.println("<hr>" + ex.getMessage() + "<hr>");
    }

    Statement stmt = null;


    // update personal info if submitted
    if( (request.getParameter("newFirst") != null && request.getParameter("newLast") != null) || request.getParameter("newAddress") != null || request.getParameter("newEmail") != null || request.getParameter("newPhone") != null) {

        if(request.getParameter("newFirst") != null && request.getParameter("newLast") != null) {

            String sqlName = "UPDATE persons SET first_name = '" + request.getParameter("newFirst") + "', last_name = '" + request.getParameter("newLast") + "' WHERE person_id ='"+person_id+"'";

            try{
                stmt = conn.createStatement();
                stmt.executeUpdate(sqlName);
                conn.commit();

            } catch(Exception ex){
                out.println("<hr>" + ex.getMessage() + "<hr>");
            }
        }

        if(request.getParameter("newAddress") != null) {

            String sqlAddress = "UPDATE persons SET address = '" + request.getParameter("newAddress") + "' WHERE person_id ='"+person_id+"'";

            try{
                stmt = conn.createStatement();
                stmt.executeUpdate(sqlAddress);
                conn.commit();

            } catch(Exception ex){
                out.println("<hr>" + ex.getMessage() + "<hr>");
            }
        }

        if(request.getParameter("newEmail") != null) {

            String sqlEmail = "UPDATE persons SET email = '" + request.getParameter("newEmail") + "' WHERE person_id ='"+person_id+"'";

            try{
                stmt = conn.createStatement();
                stmt.executeUpdate(sqlEmail);
                conn.commit();

            } catch(Exception ex){
                out.println("<hr>" + ex.getMessage() + "<hr>");
            }
        }

        if(request.getParameter("newPhone") != null) {

            String sqlPhone = "UPDATE persons SET phone = '" + request.getParameter("newPhone") + "' WHERE person_id ='"+person_id+"'";

            try{
                stmt = conn.createStatement();
                stmt.executeUpdate(sqlPhone);
                conn.commit();

            } catch(Exception ex){
                out.println("<hr>" + ex.getMessage() + "<hr>");
            }
        }
    }

    String sql = "SELECT first_name, last_name, address, email, phone FROM persons, users WHERE users.person_id = persons.person_id AND user_name = '"+userName+"'";

    String firstName = "";
    String lastName = "";
    String address = "";
    String email = "";
    String phone = "";

    try{
        stmt = conn.createStatement();
        ResultSet res = stmt.executeQuery(sql);

        while(res.next()) {
            firstName = res.getString("first_name");
            lastName = res.getString("last_name");
            address = res.getString("address");
            email = res.getString("email");
            phone = res.getString("phone");
        }

        //success
        out.println("<H1><CENTER>Personal Info</CENTER></H1>");
        out.println("<form method=post action=homePage.jsp>");
        out.println("<input type=submit name=backInfo value=Back>");
        out.println("</form>");

        out.println("<p>Name: " + firstName + " " + lastName + "</p>");
        out.println("<form method=post action=changeInfo.jsp>");
        out.println("New First Name: <input type=text name=newFirst maxlength=20><br>");
        out.println("New Last Name: <input type=text name=newLast maxlength=20><br>");
        out.println("<input type=submit name=nameSubmit value=UpdateName>");
        out.println("</form>");

        out.println("<p>address: " + address + "</p>");
        out.println("<form method=post action=changeInfo.jsp>");
        out.println("New Address: <input type=text name=newAddress maxlength=20><br>");
        out.println("<input type=submit name=addressSubmit value=UpdateAddress>");
        out.println("</form>");

        out.println("<p>email: " + email + "</p>");
        out.println("<form method=post action=changeInfo.jsp>");
        out.println("New Email: <input type=text name=newEmail maxlength=20><br>");
        out.println("<input type=submit name=emailSubmit value=UpdateEmail>");
        out.println("</form>");

        out.println("<p>phone: " + phone + "</p>");
        out.println("<form method=post action=changeInfo.jsp>");
        out.println("New Phone Number: <input type=text name=newPhone maxlength=20><br>");
        out.println("<input type=submit name=phoneSubmit value=UpdatePhone>");
        out.println("</form>");

        try {
            conn.close();
        } catch(Exception ex){
            out.println("<hr>" + ex.getMessage() + "<hr>");
        }


    } catch(Exception ex){
        out.println("<hr>" + ex.getMessage() + "<hr>");
    }

%>

</Body>
</HTML>