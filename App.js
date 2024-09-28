const handleSendMessage = async (inputText) => {
  try {
    const response = await fetch('https://taeflask-jgx3sub2o-amr-elhadys-projects.vercel.app/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: inputText }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    // Clear the conversation first
    setConversation([]);

    // Add a delay before setting the new response
    setTimeout(() => {
      setConversation([
        { role: 'assistant', content: data.response },
      ]);
    }, 1000); // Adjust the delay time (in milliseconds) as needed
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
  }
};