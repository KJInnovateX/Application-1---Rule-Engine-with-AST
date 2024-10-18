$(document).ready(function() {
    // Handle rule creation
    $('#create-rule-form').submit(function(event) {
        event.preventDefault();
        const ruleString = $('#rule').val();

        $.ajax({
            type: 'POST',
            url: '/create_rule',
            contentType: 'application/json',
            data: JSON.stringify({ rule_string: ruleString }),
            success: function(response) {
                if (response.status === 'success') {
                    alert('Rule created successfully');
                    console.log(response.ast);
                    
                    // Display the created rule
                    $('#created-rule-text').text(ruleString);
                    
                    // Set the AST in the evaluation form
                    $('#ast').val(JSON.stringify(response.ast, null, 2));
                } else {
                    alert('Error: ' + response.message);
                }
            },
            error: function(error) {
                alert('Error creating rule: ' + error.responseJSON.message);
                console.log(error);
            }
        });
    });

    // Handle rule evaluation
    $('#evaluate-rule-form').submit(function(event) {
        event.preventDefault();
        const ast = $('#ast').val();
        const data = $('#data').val();

        try {
            const parsedAST = JSON.parse(ast);
            const parsedData = JSON.parse(data);

            $.ajax({
                type: 'POST',
                url: '/evaluate_rule',
                contentType: 'application/json',
                data: JSON.stringify({ ast: parsedAST, data: parsedData }),
                success: function(response) {
                    if (response.status === 'success') {
                        $('#result').text('Result: ' + response.result);
                        if (response.result) {
                            $('#result').removeClass('result-false').addClass('result-true');
                        } else {
                            $('#result').removeClass('result-true').addClass('result-false');
                        }
                    } else {
                        alert('Error: ' + response.message);
                    }
                },
                error: function(error) {
                    alert('Error evaluating rule: ' + error.responseJSON.message);
                    console.log(error);
                }
            });
        } catch (e) {
            alert('Invalid JSON format in AST or Data.');
        }
    });


        // Reset rules from frontend and backend
        $('#reset-rules').click(function() {
            $.ajax({
                type: 'POST',
                url: '/reset_rules',
                success: function(response) {
                    if (response.status === 'success') {
                        // Clear all fields and reset frontend
                        $('#rule').val(''); // Clear rule input
                        $('#created-rule-text').text('No rule created yet.'); // Reset created rule text
                        $('#ast').val(''); // Clear AST input
                        $('#data').val(''); // Clear data input
                        $('#result').text(''); // Clear result display
                        $('#result').removeClass('result-true result-false'); // Remove result classes
                        alert('All rules have been reset successfully.');
                    } else {
                        alert('Error resetting rules: ' + response.message);
                    }
                },
                error: function(error) {
                    alert('Error resetting rules: ' + error.responseJSON.message);
                    console.log(error);
                }
            });
        });
   
    
    
 
});
