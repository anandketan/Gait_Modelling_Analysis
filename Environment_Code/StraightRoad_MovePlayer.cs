using UnityEngine;
using System.Collections;

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using UnityEngine.SceneManagement;

public class UDPReceive : MonoBehaviour
{

    // receiving Thread
    Thread receiveThread;

    // udpclient object
    UdpClient client;

    // public
    // public string IP = "127.0.0.1"; default local
    private int port; // define > init

    // infos
    private string lastReceivedUDPPacket = "";
    private string allReceivedUDPPackets = ""; // clean up this from time to time!
    private string firstChar;
    public string movement;

    //private float movementSpeed = 5f;
    // start from shell
    private static void Main()
    {
        UDPReceive receiveObj = new UDPReceive();
        receiveObj.init();

        string text = "";
        do
        {
            text = Console.ReadLine();
        }
        while (!text.Equals("exit"));
    }
    // start from unity3d
    public void Start()
    {

        init();

    }

    // OnGUI
    void OnGUI()
    {
        Rect rectObj = new Rect(40, 10, 200, 400);
        GUIStyle style = new GUIStyle();
        style.alignment = TextAnchor.UpperLeft;
        /*GUI.Box(rectObj, "# UDPReceive\n192.168.0.1 " + port + " #\n"
                    + "shell> nc -u 192.168.0.1 : " + port + " \n"
                    + "\nLast Packet: \n" + lastReceivedUDPPacket
                    + "\n\nAll Messages: \n" + allReceivedUDPPackets
                , style);
        GUI.Box(rectObj, "\nLast Packet: \n" + lastReceivedUDPPacket
                    + "\n\nAll Messages: \n" + allReceivedUDPPackets
                , style);*/

        movement = lastReceivedUDPPacket;
        firstChar = lastReceivedUDPPacket.Substring(0,2);

        /*if (string.Compare(movement, "B") == 0)
        {
            transform.Translate(0,0,0);
        }*/

        if (string.Compare(firstChar, "F1") == 0)
        {
            if (string.Compare(movement, "F1-L1") == 0)
            {
                transform.Translate(Vector3.forward * Time.deltaTime * 5);
                Vector3 playerPosition = transform.position;
                playerPosition.x -= 0.5f * Time.deltaTime * 5;
                transform.position = playerPosition;
            }
        
            else if (string.Compare(movement, "F1-L2") == 0)
            {
                transform.Translate(Vector3.forward * Time.deltaTime * 5);
                Vector3 playerPosition = transform.position;
                playerPosition.x -= 0.5f * Time.deltaTime * 15;
                transform.position = playerPosition;
            }

            else if (string.Compare(movement, "F1-R1") == 0)
            {
                transform.Translate(Vector3.forward * Time.deltaTime * 5);
                Vector3 playerPosition = transform.position;
                playerPosition.x += 0.5f * Time.deltaTime * 5;
                transform.position = playerPosition;
            }
        
            else if (string.Compare(movement, "F1-R2") == 0)
            {
                transform.Translate(Vector3.forward * Time.deltaTime * 5);
                Vector3 playerPosition = transform.position;
                playerPosition.x += 0.5f * Time.deltaTime * 15;
                transform.position = playerPosition;
            }

            else
            {
                transform.Translate(Vector3.forward * Time.deltaTime * 5);
            }
        }

        if (string.Compare(firstChar, "F2") == 0)
        {
            if (string.Compare(movement, "F2-L1") == 0)
            {
                transform.Translate(Vector3.forward * Time.deltaTime * 15);
                Vector3 playerPosition = transform.position;
                playerPosition.x -= 0.5f * Time.deltaTime * 5;
                transform.position = playerPosition;
            }
        
            else if (string.Compare(movement, "F2-L2") == 0)
            {
                transform.Translate(Vector3.forward * Time.deltaTime * 15);
                Vector3 playerPosition = transform.position;
                playerPosition.x -= 0.5f * Time.deltaTime * 15;
                transform.position = playerPosition;
            }        

            else if (string.Compare(movement, "F2-R1") == 0)
            {
                transform.Translate(Vector3.forward * Time.deltaTime * 15);
                Vector3 playerPosition = transform.position;
                playerPosition.x += 0.5f * Time.deltaTime * 5;
                transform.position = playerPosition;
            }
        
            else if (string.Compare(movement, "F2-R2") == 0)
            {
                transform.Translate(Vector3.forward * Time.deltaTime * 15);
                Vector3 playerPosition = transform.position;
                playerPosition.x += 0.5f * Time.deltaTime * 15;
                transform.position = playerPosition;
            }

            else
            {
                transform.Translate(Vector3.forward * Time.deltaTime * 15);
            }
        }        

        if (string.Compare(firstChar, "Re") == 0)
        {
            if (string.Compare(movement, "Re-L1") == 0)
            {
                transform.Translate(-Vector3.forward * Time.deltaTime * 5);
                Vector3 playerPosition = transform.position;
                playerPosition.x -= 0.5f * Time.deltaTime * 5;
                transform.position = playerPosition;
            }
        
            else if (string.Compare(movement, "Re-L2") == 0)
            {
                transform.Translate(-Vector3.forward * Time.deltaTime * 5);
                Vector3 playerPosition = transform.position;
                playerPosition.x -= 0.5f * Time.deltaTime * 15;
                transform.position = playerPosition;
            }

            else if (string.Compare(movement, "Re-R1") == 0)
            {
                transform.Translate(-Vector3.forward * Time.deltaTime * 5);
                Vector3 playerPosition = transform.position;
                playerPosition.x += 0.5f * Time.deltaTime * 5;
                transform.position = playerPosition;
            }
        
            else if (string.Compare(movement, "Re-R2") == 0)
            {
                transform.Translate(-Vector3.forward * Time.deltaTime * 5);
                Vector3 playerPosition = transform.position;
                playerPosition.x += 0.5f * Time.deltaTime * 15;
                transform.position = playerPosition;
            }
            
            else
            {
                transform.Translate(-Vector3.forward * Time.deltaTime * 5);
            }
        }        

        if (string.Compare(movement, "L1") == 0)
        {
            Vector3 playerPosition = transform.position;
            playerPosition.x -= 0.5f * Time.deltaTime * 5;
            transform.position = playerPosition;
        }
        
        if (string.Compare(movement, "L2") == 0)
        {
            Vector3 playerPosition = transform.position;
            playerPosition.x -= 0.5f * Time.deltaTime * 15;
            transform.position = playerPosition;
        }

        if (string.Compare(movement, "R1") == 0)
        {
            Vector3 playerPosition = transform.position;
            playerPosition.x += 0.5f * Time.deltaTime * 5;
            transform.position = playerPosition;
        }
        
        if (string.Compare(movement, "R2") == 0)
        {
            Vector3 playerPosition = transform.position;
            playerPosition.x += 0.5f * Time.deltaTime * 15;
            transform.position = playerPosition;
        }        
    }
    void OnTriggerEnter(Collider col)
    {
        if (col.gameObject.tag == "Wall")
        {
            SceneManager.LoadScene("GameOver");
        }
        if (col.gameObject.tag == "Finish")
        {
            SceneManager.LoadScene("YouWon");
        }
    }

    // init
    private void init()
    {
        //print("UDPSend.init()");

        // define port
        port = 5065;

        // status
        /*print("Sending to 192.168.0.1 : " + port);
        print("Test-Sending to this Port: nc -u 192.168.0.1  " + port + "");*/


        receiveThread = new Thread(
            new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();


    }

    // receive thread
    private void ReceiveData()
    {

        client = new UdpClient(port);
        while (true)
        {

            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] data = client.Receive(ref anyIP);

                string text = Encoding.UTF8.GetString(data);

                print(">> " + text);

                // latest UDPpacket
                lastReceivedUDPPacket = text;

                // ....
                allReceivedUDPPackets = allReceivedUDPPackets + text;

            }
            catch (Exception err)
            {
                print(err.ToString());
            }
        }

    }

    // getLatestUDPPacket
    // cleans up the rest
    public string getLatestUDPPacket()
    {
        allReceivedUDPPackets = "";
        return lastReceivedUDPPacket;
    }
}
