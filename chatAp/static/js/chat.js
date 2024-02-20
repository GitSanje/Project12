document.addEventListener("DOMContentLoaded", function() {
    fetch('/get_other_users_data/')
        .then(response => response.json())
        .then(otherUsers => {
            console.log(otherUsers);

            let input_message = $('#input-message');
            let send_message_form = $('#send-message-form');
            const USER_ID = $('#logged-in-user').val();
            let message_body = $('.msg_card_body');

            let loc = window.location;
            let wsStart = 'ws://';

            if (loc.protocol === 'https:') {
                wsStart = 'wss://';
            }
            let endpoint = wsStart + loc.host + loc.pathname;

            var socket = new WebSocket(endpoint);

            socket.onopen = async function(e) {
                console.log('WebSocket connection opened');
                send_message_form.on('submit', function(e) {
                    e.preventDefault();
                    let message = input_message.val();
                    let send_to = get_active_other_user_id();
                    let thread_id = get_active_thread_id();
                    let data = {
                        'message': message,
                        'sent_by': USER_ID,
                        'send_to': send_to,
                        'thread_id': thread_id
                    };
                    data = JSON.stringify(data);
                    socket.send(data);
                    $(this)[0].reset();
                });
            };

            socket.onmessage = async function(e) {
                console.log('WebSocket message received:', e);
                try {
                    let data = JSON.parse(e.data);
                    let message = data['message'];
                    let sent_by_id = data['sent_by'];
                    let thread_id = data['thread_id'];

                    let otherUserProfileImageUrl = otherUsers[thread_id].profile_image_url;
                    let otherUserFullName = otherUsers[thread_id].full_name;
                    let UserProfileImageUrl = otherUsers['request_user'].profile_image_url;
                    console.log("Other user profile:", otherUserProfileImageUrl, "Other user name:", otherUserFullName, UserProfileImageUrl);

                    newMessage(message, sent_by_id, thread_id, otherUserProfileImageUrl, otherUserFullName,UserProfileImageUrl);
                } catch (error) {
                    console.error('Error parsing WebSocket data:', error);
                }
            };

            function newMessage(message, sent_by_id, thread_id, otherUserProfileImageUrl, otherUserFullName,UserProfileImageUrl) {
                let chatMessageContainer = $(`.messages-wrapper[chat-id="chat_${thread_id}"] .chat-messages`);
                let isCurrentUser = sent_by_id == USER_ID;
                let messageClass = isCurrentUser ? 'chat-message-right' : 'chat-message-left';

                let messageHTML = `
                    <div class="${messageClass} pb-4">
                        <div>
                            <img src="${isCurrentUser ? UserProfileImageUrl : otherUserProfileImageUrl}"
                                class="rounded-circle mr-1"
                                alt=""
                                width="40"
                                height="40"/>
                            <div class="text-muted small text-nowrap mt-2">${getCurrentDateTime()}</div>
                        </div>
                        <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
                            <div class="font-weight-bold mb-1">${isCurrentUser ? 'You' : otherUserFullName}</div>
                            ${message}
                        </div>
                    </div>`;

                chatMessageContainer.append(messageHTML);
                chatMessageContainer.scrollTop(chatMessageContainer.prop("scrollHeight"));
            }

           function getCurrentDateTime() {
                let now = new Date();


              let months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                let date = `${now.getDate().toString().padStart(2, '0')}`;

                 let month = months[now.getMonth()];
                let time = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;

                return `${date} ${month}, ${time}`;
            }


            socket.onerror = async function(e) {
                console.log('WebSocket error:', e);
            };

            socket.onclose = async function(e) {
                console.log('WebSocket connection closed:', e);
            };
        })
        .catch(error => console.log('Error fetching otherUsers data:', error));
});


$(document).ready(function() {

      function searchFunction() {
        var input, filter, ul, li, div, i, txtValue;
        input = document.getElementById("searchInput");
        filter = input.value.toUpperCase();
        ul = document.querySelector(".contacts");
        li = ul.getElementsByTagName("li");

        // Loop through all list items, and hide those that don't match the search query
        for (i = 0; i < li.length; i++) {
            div = li[i].querySelector(".flex-grow-1.ml-3");
            txtValue = div.textContent || div.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                li[i].style.display = "";
            } else {
                li[i].style.display = "none";
            }
        }
    }

    // When a contact is clicked
    $('.contact-li').on('click', function (){
        // Remove 'active' class from all contacts
        $('.contact-li').removeClass('active');
        // Add 'active' class to the clicked contact
        $(this).addClass('active');

        // Get the chat ID associated with the clicked contact
        let chatId = $(this).attr('chat-id');

        // Remove 'is_active' class from all message wrappers
        $('.messages-wrapper').removeClass('is_active');
        // Add 'is_active' class to the message wrapper corresponding to the clicked contact
        $('.messages-wrapper[chat-id="' + chatId + '"]').addClass('is_active');

        // Store the active chat ID in local storage
        localStorage.setItem('activeChatId', chatId.replace('chat_', ''));
    });
     // Get the active chat thread ID from local storage
    let activeChatId = localStorage.getItem('activeChatId');

    // If there's an active chat ID stored, set the corresponding profile as active
    if (activeChatId) {
        let activeContact = $('.contact-li[chat-id="chat_' + activeChatId + '"]');
        if (activeContact.length > 0) {
            // Remove 'active' class from all contacts
            $('.contact-li').removeClass('active');
            // Add 'active' class to the active contact
            activeContact.addClass('active');

            // Set the corresponding message wrapper as active
            let chatId = activeContact.attr('chat-id');
            $('.messages-wrapper').removeClass('is_active');
            $('.messages-wrapper[chat-id="' + chatId + '"]').addClass('is_active');
        }
    }

    $('#searchInput').on('input', function() {
        searchFunction();
    });
});





function get_active_other_user_id(){
    let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}

function get_active_thread_id(){
    let chat_id = $('.messages-wrapper.is_active').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}


